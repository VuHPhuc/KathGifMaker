# video_processor.py
import cv2
import os
from PIL import Image
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QImage

class VideoInfoWorker(QThread):
    """Worker thread to quickly extract video details (duration, native FPS, dimensions)."""
    info_ready = Signal(dict)
    error_occurred = Signal(str)

    def __init__(self, video_path):
        super().__init__()
        self.video_path = video_path

    def run(self):
        try:
            cap = cv2.VideoCapture(self.video_path)
            if not cap.isOpened():
                self.error_occurred.emit("Không thể mở video.")
                return

            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            duration = frame_count / fps if fps > 0 else 0

            cap.release()
            self.info_ready.emit({
                "fps": fps,
                "frame_count": frame_count,
                "width": width,
                "height": height,
                "duration": duration
            })
        except Exception as e:
            self.error_occurred.emit(str(e))


class FrameExtractWorker(QThread):
    """Worker thread to extract frames from a video at specific intervals."""
    progress = Signal(int)
    frame_extracted = Signal(dict)
    finished = Signal(list)
    error_occurred = Signal(str)

    def __init__(self, video_path, start_time, end_time, target_fps, max_preview_dim=960, max_thumb_dim=160):
        super().__init__()
        self.video_path = video_path
        self.start_time = start_time
        self.end_time = end_time
        self.target_fps = target_fps
        self.max_preview_dim = max_preview_dim
        self.max_thumb_dim = max_thumb_dim
        self._is_cancelled = False

    def cancel(self):
        self._is_cancelled = True

    def run(self):
        try:
            cap = cv2.VideoCapture(self.video_path)
            if not cap.isOpened():
                self.error_occurred.emit("Không thể mở video.")
                return

            native_fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
            
            if native_fps <= 0:
                native_fps = 25.0

            video_duration = total_frames / native_fps
            start_sec = max(0.0, min(self.start_time, video_duration))
            end_sec = max(start_sec, min(self.end_time, video_duration))

            start_frame = int(start_sec * native_fps)
            end_frame = int(end_sec * native_fps)
            
            # Prevent single frame slice crash
            if end_frame <= start_frame:
                end_frame = min(int(total_frames), start_frame + 1)

            # Determine frame index steps
            # native_fps = 30, target_fps = 10 -> step = 3
            step = max(1.0, native_fps / self.target_fps)
            
            target_indices = []
            curr = float(start_frame)
            while curr < end_frame:
                idx = int(round(curr))
                if idx < total_frames:
                    if not target_indices or target_indices[-1] != idx:
                        target_indices.append(idx)
                curr += step

            if not target_indices:
                self.error_occurred.emit("Không tìm thấy frame nào để trích xuất trong khoảng thời gian đã chọn.")
                cap.release()
                return

            extracted_frames = []
            total_targets = len(target_indices)

            for i, frame_idx in enumerate(target_indices):
                if self._is_cancelled:
                    break

                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
                ret, frame = cap.read()
                if not ret:
                    continue

                # cv2 to RGB
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, _ = rgb_frame.shape

                # Scale helper for QImage creation
                def scale_img(img, max_dim):
                    sh, sw = img.shape[:2]
                    if sw > max_dim or sh > max_dim:
                        if sw > sh:
                            new_w = max_dim
                            new_h = int(sh * (max_dim / sw))
                        else:
                            new_h = max_dim
                            new_w = int(sw * (max_dim / sh))
                        return cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
                    return img

                preview_cv = scale_img(rgb_frame, self.max_preview_dim)
                thumb_cv = scale_img(rgb_frame, self.max_thumb_dim)

                ph, pw, _ = preview_cv.shape
                th, tw, _ = thumb_cv.shape

                # Convert to safe QImages via copy
                preview_qimg = QImage(preview_cv.data, pw, ph, 3 * pw, QImage.Format_RGB888).copy()
                thumb_qimg = QImage(thumb_cv.data, tw, th, 3 * tw, QImage.Format_RGB888).copy()

                frame_data = {
                    "index": i,
                    "frame_num": frame_idx,
                    "timestamp": frame_idx / native_fps,
                    "preview": preview_qimg,
                    "thumbnail": thumb_qimg,
                    "enabled": True
                }
                
                extracted_frames.append(frame_data)
                self.frame_extracted.emit(frame_data)

                # Progress
                prog = int(((i + 1) / total_targets) * 100)
                self.progress.emit(prog)

            cap.release()
            
            if self._is_cancelled:
                self.error_occurred.emit("Đã hủy quá trình trích xuất.")
            else:
                self.finished.emit(extracted_frames)

        except Exception as e:
            self.error_occurred.emit(str(e))


class GifExportWorker(QThread):
    """Worker thread to assemble and export selected frames as an animated GIF."""
    progress = Signal(int)
    finished = Signal(str)
    error_occurred = Signal(str)

    def __init__(self, video_path, frame_numbers, output_path, gif_width, gif_height, frame_delay_ms, loop_count=0):
        super().__init__()
        self.video_path = video_path
        self.frame_numbers = frame_numbers  # list of source video frame numbers
        self.output_path = output_path
        self.gif_width = gif_width
        self.gif_height = gif_height
        self.frame_delay_ms = frame_delay_ms  # delay in ms per frame
        self.loop_count = loop_count

    def run(self):
        try:
            if not self.frame_numbers:
                self.error_occurred.emit("Không có frame nào để xuất GIF.")
                return

            cap = cv2.VideoCapture(self.video_path)
            if not cap.isOpened():
                self.error_occurred.emit("Không thể mở video gốc để xuất GIF.")
                return

            pil_images = []
            total_frames = len(self.frame_numbers)

            for i, f_num in enumerate(self.frame_numbers):
                cap.set(cv2.CAP_PROP_POS_FRAMES, f_num)
                ret, frame = cap.read()
                if not ret:
                    continue

                # Convert BGR to RGB
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Convert to PIL Image
                pil_img = Image.fromarray(rgb_frame)
                
                # Resize if dimensions differ from original
                orig_w, orig_h = pil_img.size
                w = self.gif_width if self.gif_width > 0 else orig_w
                h = self.gif_height if self.gif_height > 0 else orig_h
                
                if (w, h) != (orig_w, orig_h):
                    pil_img = pil_img.resize((w, h), Image.Resampling.LANCZOS)
                
                pil_images.append(pil_img)
                
                # Update progress
                prog = int(((i + 1) / total_frames) * 90)  # up to 90% for reading
                self.progress.emit(prog)

            cap.release()

            if not pil_images:
                self.error_occurred.emit("Không thể đọc được frame nào từ video.")
                return

            # Save as animated GIF
            # PIL requires duration in milliseconds
            self.progress.emit(95)
            pil_images[0].save(
                self.output_path,
                save_all=True,
                append_images=pil_images[1:],
                duration=self.frame_delay_ms,
                loop=self.loop_count,
                optimize=True
            )
            
            self.progress.emit(100)
            self.finished.emit(self.output_path)

        except Exception as e:
            self.error_occurred.emit(str(e))

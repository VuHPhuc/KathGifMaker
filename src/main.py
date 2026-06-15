# main.py
import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QSlider, QSpinBox, QFileDialog, QListWidget,
    QListWidgetItem, QProgressBar, QCheckBox, QFrame, QMessageBox,
    QSplitter, QGroupBox, QGraphicsOpacityEffect, QScrollArea, QSizePolicy,
    QComboBox, QRadioButton, QStatusBar
)
from PySide6.QtCore import Qt, QTimer, Slot, QSize, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QPixmap, QIcon, QImage, QPainter, QFont

from styles import QSS_STYLE
from icons import get_svg_icon, HAS_SVG
from video_processor import VideoInfoWorker, FrameExtractWorker, GifExportWorker

class FrameCardWidget(QWidget):
    """Custom widget representing a frame item in the sidebar."""
    toggled = Slot(int, bool)
    deleted = Slot(int)

    def __init__(self, frame_data, parent=None):
        super().__init__(parent)
        self.frame_data = frame_data
        self.index = frame_data["index"]
        self.frame_num = frame_data["frame_num"]
        self.enabled = True

        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(8)

        # Checkbox
        self.checkbox = QCheckBox(self)
        self.checkbox.setChecked(True)
        self.checkbox.stateChanged.connect(self.on_checkbox_changed)
        layout.addWidget(self.checkbox)

        # Thumbnail
        self.thumb_label = QLabel(self)
        pix = QPixmap.fromImage(self.frame_data["thumbnail"])
        self.thumb_label.setPixmap(pix)
        self.thumb_label.setFixedSize(70, 50)
        self.thumb_label.setScaledContents(True)
        layout.addWidget(self.thumb_label)

        # Labels
        meta_layout = QVBoxLayout()
        meta_layout.setSpacing(2)
        
        self.lbl_num = QLabel(f"Frame #{self.frame_data['index'] + 1}", self)
        self.lbl_num.setStyleSheet("font-weight: bold; color: #a5b4fc;")
        meta_layout.addWidget(self.lbl_num)

        self.lbl_time = QLabel(f"T: {self.frame_data['timestamp']:.2f}s", self)
        self.lbl_time.setStyleSheet("color: #94a3b8; font-size: 11px;")
        meta_layout.addWidget(self.lbl_time)

        layout.addLayout(meta_layout)
        layout.addStretch()

        # Delete Button
        self.btn_del = QPushButton(self)
        self.btn_del.setFixedSize(24, 24)
        self.btn_del.setToolTip("Xóa frame này")
        if HAS_SVG:
            self.btn_del.setIcon(get_svg_icon("trash", size=QSize(14, 14), color="#f87171"))
            self.btn_del.setStyleSheet(
                "QPushButton { background-color: transparent; border: none; }"
                "QPushButton:hover { background-color: rgba(248, 113, 113, 0.15); border-radius: 4px; }"
            )
        else:
            self.btn_del.setText("✕")
            self.btn_del.setStyleSheet(
                "QPushButton { background-color: transparent; border: none; color: #f87171; font-weight: bold; font-size: 14px; }"
                "QPushButton:hover { background-color: rgba(248, 113, 113, 0.15); border-radius: 4px; }"
            )
        self.btn_del.clicked.connect(self.on_delete_clicked)
        layout.addWidget(self.btn_del)

        # Transparency for toggling frames
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)

    def on_checkbox_changed(self, state):
        self.enabled = self.checkbox.isChecked()
        self.opacity_effect.setOpacity(1.0 if self.enabled else 0.4)
        
        # Access parent MainWindow to trigger toggling
        main_win = self.window()
        if hasattr(main_win, "toggle_frame"):
            main_win.toggle_frame(self.index, self.enabled)

    def on_delete_clicked(self):
        main_win = self.window()
        if hasattr(main_win, "delete_frame"):
            main_win.delete_frame(self.index)


def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        # main.py is in src/, so dev mode resources are in src/
        base_path = os.path.dirname(os.path.abspath(__file__))
        if not os.path.exists(os.path.join(base_path, relative_path)):
            base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_app_root():
    """ Get root directory of the application """
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        # main.py is in src/, so parent of src/ is the workspace root
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class AspectRatioPixmapLabel(QLabel):
    """Custom label that scales and centers the pixmap dynamically without stretching the layout."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.raw_pixmap = None
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.setAlignment(Qt.AlignCenter)

    def setPixmap(self, pixmap):
        self.raw_pixmap = pixmap
        self.update()

    def paintEvent(self, event):
        # Draw base styles/borders
        super().paintEvent(event)
        
        if self.raw_pixmap and not self.raw_pixmap.isNull():
            painter = QPainter(self)
            # Calculate aspect ratio scale to fit label widget size
            scaled_pix = self.raw_pixmap.scaled(
                self.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            # Center coordinates
            x = (self.width() - scaled_pix.width()) // 2
            y = (self.height() - scaled_pix.height()) // 2
            painter.drawPixmap(x, y, scaled_pix)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KathGifMaker - Trình Tạo GIF Chuyên Nghiệp")
        self.resize(1280, 820)
        self.setMinimumSize(1000, 680)
        
        # Set Window Icon
        icon_path = get_resource_path("app_icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        self.video_path = ""
        self.video_info = {}
        self.all_frames = []      # list of frame dicts
        self.current_frame = None
        
        # Playback Preview Timer
        self.preview_timer = QTimer(self)
        self.preview_timer.timeout.connect(self.play_next_frame)
        self.current_preview_idx = 0
        
        # Worker threads
        self.info_worker = None
        self.extract_worker = None
        self.export_worker = None

        self.init_ui()
        self.setStyleSheet(QSS_STYLE)
        self.setAcceptDrops(True)

    def init_ui(self):
        root_widget = QWidget(self)
        self.setCentralWidget(root_widget)

        root_layout = QVBoxLayout(root_widget)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # ── App Title Bar ──────────────────────────────────────────────────
        self.init_title_bar(root_layout)

        # ── Content Area ───────────────────────────────────────────────────
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(10, 10, 10, 10)
        content_layout.setSpacing(10)
        root_layout.addWidget(content_widget, 1)

        # Splitter Layout
        self.splitter = QSplitter(Qt.Horizontal, self)
        content_layout.addWidget(self.splitter)

        # 1. Left Sidebar (Frames list)
        self.init_left_sidebar()
        
        # 2. Center Panel (GIF/Image Preview)
        self.init_center_panel()

        # 3. Right Panel (Controls & Parameters)
        self.init_right_panel()

        # Set constraints on sidebar panels
        self.left_frame.setMinimumWidth(265)
        self.left_frame.setMaximumWidth(370)
        self.right_frame.setMinimumWidth(295)
        self.right_frame.setMaximumWidth(390)

        # Add to splitter and set sizes
        self.splitter.addWidget(self.left_frame)
        self.splitter.addWidget(self.center_frame)
        self.splitter.addWidget(self.right_frame)
        self.splitter.setSizes([290, 660, 290])

        # ── Status Bar ─────────────────────────────────────────────────────
        self.init_status_bar(root_layout)

    def init_title_bar(self, parent_layout):
        """Stylish app header bar."""
        title_bar = QFrame()
        title_bar.setObjectName("appTitleBar")
        title_bar.setFixedHeight(52)
        tb_layout = QHBoxLayout(title_bar)
        tb_layout.setContentsMargins(16, 0, 16, 0)
        tb_layout.setSpacing(10)

        # App icon (film reel)
        if HAS_SVG:
            icon_lbl = QLabel()
            icon_lbl.setFixedSize(30, 30)
            pix = get_svg_icon("film", size=QSize(28, 28), color="#818cf8").pixmap(QSize(28, 28))
            icon_lbl.setPixmap(pix)
            icon_lbl.setAlignment(Qt.AlignCenter)
            tb_layout.addWidget(icon_lbl)

        # Title + subtitle
        text_layout = QVBoxLayout()
        text_layout.setSpacing(1)
        text_layout.setContentsMargins(0, 0, 0, 0)

        title_lbl = QLabel("KathGifMaker")
        title_lbl.setObjectName("appTitleLabel")
        title_lbl.setFont(QFont("Segoe UI Variable", 15, QFont.Bold))
        text_layout.addWidget(title_lbl)

        subtitle_lbl = QLabel("TRÌNH TẠO GIF CHUYÊN NGHIỆP")
        subtitle_lbl.setObjectName("appSubtitleLabel")
        subtitle_lbl.setFont(QFont("Segoe UI", 9))
        text_layout.addWidget(subtitle_lbl)

        tb_layout.addLayout(text_layout)

        # Version badge
        version_lbl = QLabel("v2.0")
        version_lbl.setObjectName("appVersionBadge")
        version_lbl.setFixedHeight(22)
        tb_layout.addWidget(version_lbl)

        tb_layout.addStretch(1)

        # Sparkles icon on right
        if HAS_SVG:
            spark_lbl = QLabel()
            spark_lbl.setFixedSize(24, 24)
            pix2 = get_svg_icon("sparkles", size=QSize(20, 20), color="#4f46e5").pixmap(QSize(20, 20))
            spark_lbl.setPixmap(pix2)
            spark_lbl.setAlignment(Qt.AlignCenter)
            tb_layout.addWidget(spark_lbl)

        parent_layout.addWidget(title_bar)

    def init_status_bar(self, parent_layout):
        """Stylish bottom status bar."""
        status_bar = QFrame()
        status_bar.setObjectName("statusBar")
        status_bar.setFixedHeight(30)
        sb_layout = QHBoxLayout(status_bar)
        sb_layout.setContentsMargins(16, 0, 16, 0)
        sb_layout.setSpacing(16)

        # Dot indicator
        self.status_dot = QLabel("●")
        self.status_dot.setStyleSheet("color: #1a3a5e; font-size: 10px;")
        self.status_dot.setFixedWidth(14)
        sb_layout.addWidget(self.status_dot)

        self.status_label = QLabel("Sẵn sàng · Kéo và thả video vào màn hình để bắt đầu")
        self.status_label.setObjectName("statusLabel")
        sb_layout.addWidget(self.status_label)

        sb_layout.addStretch(1)

        # Right side: credit
        credit_lbl = QLabel("Made with ♥ by Kath")
        credit_lbl.setObjectName("statusLabel")
        credit_lbl.setStyleSheet("color: #1e3050; font-size: 11px;")
        sb_layout.addWidget(credit_lbl)

        parent_layout.addWidget(status_bar)

    def set_status(self, message: str, active: bool = False):
        """Update the status bar message."""
        if hasattr(self, 'status_label'):
            self.status_label.setText(message)
        if hasattr(self, 'status_dot'):
            color = "#10b981" if active else "#4a6a9a"
            self.status_dot.setStyleSheet(f"color: {color}; font-size: 10px;")

    def init_left_sidebar(self):
        self.left_frame = QFrame(self)
        self.left_frame.setObjectName("sidebarPanel")
        
        layout = QVBoxLayout(self.left_frame)
        layout.setContentsMargins(12, 14, 12, 12)
        layout.setSpacing(10)

        # Header row with icon
        header_row = QHBoxLayout()
        header_row.setSpacing(6)
        if HAS_SVG:
            hdr_icon = QLabel()
            hdr_icon.setFixedSize(16, 16)
            hdr_icon.setPixmap(get_svg_icon("layers", size=QSize(14, 14), color="#4a6a9a").pixmap(QSize(14, 14)))
            header_row.addWidget(hdr_icon)
        lbl_header = QLabel("DANH SÁCH FRAME", self)
        lbl_header.setObjectName("panelHeader")
        header_row.addWidget(lbl_header)
        header_row.addStretch()
        layout.addLayout(header_row)

        # Sidebar frame manipulation buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(6)
        
        self.btn_select_all = QPushButton(" Chọn Hết", self)
        self.btn_select_all.setIcon(get_svg_icon("check_all", size=QSize(15, 15), color="#10b981"))
        self.btn_select_all.setToolTip("Chọn tất cả frames")
        self.btn_select_all.clicked.connect(self.select_all_frames)
        btn_layout.addWidget(self.btn_select_all)
        
        self.btn_deselect_all = QPushButton(" Bỏ Chọn", self)
        self.btn_deselect_all.setIcon(get_svg_icon("uncheck_all", size=QSize(15, 15), color="#94a3b8"))
        self.btn_deselect_all.setToolTip("Bỏ chọn tất cả frames")
        self.btn_deselect_all.clicked.connect(self.deselect_all_frames)
        btn_layout.addWidget(self.btn_deselect_all)
        
        layout.addLayout(btn_layout)

        # List Widget for frames list
        self.frames_list_widget = QListWidget(self)
        self.frames_list_widget.itemClicked.connect(self.on_frame_item_clicked)
        layout.addWidget(self.frames_list_widget)

        # Frame count badge
        self.lbl_frames_count = QLabel("0 frames", self)
        self.lbl_frames_count.setObjectName("frameCountBadge")
        self.lbl_frames_count.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lbl_frames_count)

    def init_center_panel(self):
        self.center_frame = QFrame(self)
        self.center_frame.setObjectName("centerPanel")
        
        layout = QVBoxLayout(self.center_frame)
        layout.setContentsMargins(12, 14, 12, 12)
        layout.setSpacing(10)

        # Video Title / Status (header row)
        header_row = QHBoxLayout()
        header_row.setSpacing(6)
        if HAS_SVG:
            hdr_icon = QLabel()
            hdr_icon.setFixedSize(16, 16)
            hdr_icon.setPixmap(get_svg_icon("image", size=QSize(14, 14), color="#4a6a9a").pixmap(QSize(14, 14)))
            header_row.addWidget(hdr_icon)
        self.lbl_video_title = QLabel("PREVIEW", self)
        self.lbl_video_title.setObjectName("panelHeader")
        self.lbl_video_title.setWordWrap(True)
        header_row.addWidget(self.lbl_video_title)
        header_row.addStretch()
        layout.addLayout(header_row)

        # Large display area
        self.preview_label = AspectRatioPixmapLabel(self)
        self.preview_label.setStyleSheet(
            "background-color: #060c18;"
            "border: 1px solid #1a2d4a;"
            "border-radius: 12px;"
        )
        self.preview_label.setMinimumSize(420, 300)
        layout.addWidget(self.preview_label, 1)

        # Drop hint text (shown when no video)
        self.drop_hint = QLabel("🎬  Kéo & Thả video vào đây hoặc dùng 'Chọn Video'", self)
        self.drop_hint.setObjectName("dropHintLabel")
        self.drop_hint.setAlignment(Qt.AlignCenter)
        self.drop_hint.setWordWrap(True)
        layout.addWidget(self.drop_hint)

        # Timeline Slider
        slider_row = QHBoxLayout()
        slider_row.setSpacing(8)
        if HAS_SVG:
            clock_lbl = QLabel()
            clock_lbl.setFixedSize(16, 16)
            clock_lbl.setPixmap(get_svg_icon("clock", size=QSize(14, 14), color="#2a4468").pixmap(QSize(14, 14)))
            slider_row.addWidget(clock_lbl)
        self.timeline_slider = QSlider(Qt.Horizontal, self)
        self.timeline_slider.setRange(0, 0)
        self.timeline_slider.sliderMoved.connect(self.on_timeline_scrubbed)
        self.timeline_slider.setToolTip("Kéo để di chuyển qua các frame")
        slider_row.addWidget(self.timeline_slider)
        layout.addLayout(slider_row)

        # Playback controls
        playback_layout = QHBoxLayout()
        playback_layout.setSpacing(8)
        playback_layout.setAlignment(Qt.AlignCenter)

        self.btn_prev = QPushButton(self)
        self.btn_prev.setObjectName("iconButton")
        self.btn_prev.setFixedSize(40, 36)
        self.btn_prev.setToolTip("Frame trước")
        if HAS_SVG:
            self.btn_prev.setIcon(get_svg_icon("prev", size=QSize(16, 16), color="#818cf8"))
        else:
            self.btn_prev.setText("⏮")
        self.btn_prev.clicked.connect(self.prev_frame)
        playback_layout.addWidget(self.btn_prev)

        self.btn_play = QPushButton(" Phát" if HAS_SVG else "▶ Phát", self)
        self.btn_play.setObjectName("playButton")
        self.btn_play.setIcon(get_svg_icon("play", size=QSize(16, 16), color="#ffffff"))
        self.btn_play.setFixedSize(130, 36)
        self.btn_play.setToolTip("Phát / Tạm dừng preview")
        self.btn_play.clicked.connect(self.toggle_play_preview)
        playback_layout.addWidget(self.btn_play)

        self.btn_next = QPushButton(self)
        self.btn_next.setObjectName("iconButton")
        self.btn_next.setFixedSize(40, 36)
        self.btn_next.setToolTip("Frame tiếp theo")
        if HAS_SVG:
            self.btn_next.setIcon(get_svg_icon("next", size=QSize(16, 16), color="#818cf8"))
        else:
            self.btn_next.setText("⏭")
        self.btn_next.clicked.connect(self.next_frame)
        playback_layout.addWidget(self.btn_next)

        layout.addLayout(playback_layout)

        # Status of preview
        self.lbl_preview_status = QLabel("Frame: 0/0  ·  Thời gian: 0.00s", self)
        self.lbl_preview_status.setAlignment(Qt.AlignCenter)
        self.lbl_preview_status.setStyleSheet("color: #2a4468; font-size: 11px; font-weight: 500;")
        layout.addWidget(self.lbl_preview_status)

    def update_play_button_state(self, playing):
        if playing:
            self.btn_play.setText(" Tạm Dừng")
            self.btn_play.setIcon(get_svg_icon("pause", size=QSize(16, 16), color="#ffffff"))
            self.set_status("Đang phát preview...", active=True)
        else:
            self.btn_play.setText(" Phát")
            self.btn_play.setIcon(get_svg_icon("play", size=QSize(16, 16), color="#ffffff"))
            self.set_status("Đã dừng preview.", active=False)

    def init_right_panel(self):
        self.right_frame = QFrame(self)
        self.right_frame.setObjectName("rightPanel")
        
        layout = QVBoxLayout(self.right_frame)
        layout.setContentsMargins(12, 14, 12, 12)
        layout.setSpacing(10)

        # Header with icon
        header_row = QHBoxLayout()
        header_row.setSpacing(6)
        if HAS_SVG:
            hdr_icon = QLabel()
            hdr_icon.setFixedSize(16, 16)
            hdr_icon.setPixmap(get_svg_icon("settings", size=QSize(14, 14), color="#4a6a9a").pixmap(QSize(14, 14)))
            header_row.addWidget(hdr_icon)
        lbl_header = QLabel("BẢNG CHỨC NĂNG", self)
        lbl_header.setObjectName("panelHeader")
        header_row.addWidget(lbl_header)
        header_row.addStretch()
        layout.addLayout(header_row)

        # Scroll Area
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background-color: transparent; border: none;")
        scroll_content = QWidget()
        scroll_content.setStyleSheet("background-color: transparent;")
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(12)

        # ── Group 1: Select Video ──────────────────────────────────────────
        grp_video = QGroupBox("① Chọn Video Đầu Vào", self)
        video_layout = QVBoxLayout(grp_video)
        video_layout.setSpacing(8)
        video_layout.setContentsMargins(10, 14, 10, 10)
        
        self.btn_load_video = QPushButton("  Chọn Video...", self)
        self.btn_load_video.setObjectName("primaryButton")
        self.btn_load_video.setIcon(get_svg_icon("folder_open", size=QSize(16, 16), color="#ffffff"))
        self.btn_load_video.setToolTip("Mở hộp thoại chọn file video")
        self.btn_load_video.clicked.connect(self.browse_video)
        video_layout.addWidget(self.btn_load_video)

        self.lbl_video_path = QLabel("Chưa chọn file", self)
        self.lbl_video_path.setWordWrap(True)
        self.lbl_video_path.setStyleSheet(
            "color: #2a4468; font-size: 11px; padding: 2px 0px;"
        )
        video_layout.addWidget(self.lbl_video_path)

        # InfoBox for video metadata
        self.info_box = QFrame()
        self.info_box.setObjectName("infoBox")
        info_box_layout = QVBoxLayout(self.info_box)
        info_box_layout.setContentsMargins(8, 8, 8, 8)
        info_box_layout.setSpacing(4)

        self.lbl_video_meta = QLabel("Thời lượng: --  ·  Độ phân giải: --  ·  FPS: --", self)
        self.lbl_video_meta.setWordWrap(True)
        self.lbl_video_meta.setStyleSheet(
            "color: #4a6a9a; font-size: 11px; line-height: 1.6;"
        )
        info_box_layout.addWidget(self.lbl_video_meta)
        video_layout.addWidget(self.info_box)
        
        scroll_layout.addWidget(grp_video)

        # ── Group 2: Frame Extraction ──────────────────────────────────────
        self.grp_slice = QGroupBox("② Trích Xuất Frame", self)
        self.grp_slice.setEnabled(False)
        slice_layout = QVBoxLayout(self.grp_slice)
        slice_layout.setSpacing(8)
        slice_layout.setContentsMargins(10, 14, 10, 10)

        grid_layout = QHBoxLayout()
        lbl_start = QLabel("Bắt đầu (s):", self)
        lbl_start.setStyleSheet("color: #64748b; font-size: 12px;")
        self.spin_start = QSpinBox(self)
        self.spin_start.setRange(0, 99999)
        self.spin_start.setValue(0)
        self.spin_start.setToolTip("Thời điểm bắt đầu cắt (giây)")
        grid_layout.addWidget(lbl_start)
        grid_layout.addWidget(self.spin_start)
        slice_layout.addLayout(grid_layout)

        grid_layout2 = QHBoxLayout()
        lbl_end = QLabel("Kết thúc (s):", self)
        lbl_end.setStyleSheet("color: #64748b; font-size: 12px;")
        self.spin_end = QSpinBox(self)
        self.spin_end.setRange(0, 99999)
        self.spin_end.setValue(10)
        self.spin_end.setToolTip("Thời điểm kết thúc cắt (giây)")
        grid_layout2.addWidget(lbl_end)
        grid_layout2.addWidget(self.spin_end)
        slice_layout.addLayout(grid_layout2)

        grid_layout3 = QHBoxLayout()
        lbl_fps = QLabel("FPS trích xuất:", self)
        lbl_fps.setStyleSheet("color: #64748b; font-size: 12px;")
        self.spin_fps = QSpinBox(self)
        self.spin_fps.setRange(1, 60)
        self.spin_fps.setValue(10)
        self.spin_fps.setToolTip("Số lượng frame trích xuất trên 1 giây video")
        grid_layout3.addWidget(lbl_fps)
        grid_layout3.addWidget(self.spin_fps)
        slice_layout.addLayout(grid_layout3)

        self.btn_extract = QPushButton("  Trích Xuất Frame", self)
        self.btn_extract.setObjectName("primaryButton")
        self.btn_extract.setIcon(get_svg_icon("scissors", size=QSize(16, 16), color="#ffffff"))
        self.btn_extract.setToolTip("Bắt đầu trích xuất frames từ video")
        self.btn_extract.clicked.connect(self.start_frame_extraction)
        slice_layout.addWidget(self.btn_extract)

        scroll_layout.addWidget(self.grp_slice)

        # ── Group 3: GIF Output Config ─────────────────────────────────────
        self.grp_gif = QGroupBox("③ Thiết Lập GIF", self)
        self.grp_gif.setEnabled(False)
        gif_layout = QVBoxLayout(self.grp_gif)
        gif_layout.setSpacing(8)
        gif_layout.setContentsMargins(10, 14, 10, 10)

        # Mode radio selector
        mode_layout = QHBoxLayout()
        mode_layout.setSpacing(12)
        self.rad_simple = QRadioButton("  Cơ bản", self)
        self.rad_simple.setChecked(True)
        self.rad_simple.setToolTip("Chế độ đơn giản: chọn tốc độ và kích thước")
        self.rad_simple.toggled.connect(self.on_gif_mode_changed)
        self.rad_advanced = QRadioButton("  Nâng cao", self)
        self.rad_advanced.setToolTip("Chế độ nâng cao: tùy chỉnh chi tiết từng tham số")
        mode_layout.addWidget(self.rad_simple)
        mode_layout.addWidget(self.rad_advanced)
        gif_layout.addLayout(mode_layout)

        # 3.1 Simple Mode Widget
        self.simple_widget = QWidget(self)
        simple_lay = QVBoxLayout(self.simple_widget)
        simple_lay.setContentsMargins(0, 0, 0, 0)
        simple_lay.setSpacing(8)

        grid_speed = QHBoxLayout()
        lbl_speed = QLabel("Tốc độ:", self)
        lbl_speed.setStyleSheet("color: #64748b; font-size: 12px;")
        grid_speed.addWidget(lbl_speed)
        self.combo_speed = QComboBox(self)
        self.combo_speed.setToolTip("Chọn tốc độ phát GIF")
        self.combo_speed.addItems([
            "⚡ Bình thường (1.0x)",
            "🐇 Nhanh hơn (1.25x)",
            "🐇 Nhanh (1.5x)",
            "🐇 Rất nhanh (1.75x)",
            "🐇 Nhanh x2 (2.0x)",
            "⚡ Nhanh x3 (3.0x)",
            "🐢 Chậm hơn (0.75x)",
            "🐢 Chậm x0.5 (0.5x)",
            "🐢 Rất chậm (0.25x)"
        ])
        self.combo_speed.setCurrentIndex(0)
        self.combo_speed.currentIndexChanged.connect(self.on_simple_speed_changed)
        grid_speed.addWidget(self.combo_speed)
        simple_lay.addLayout(grid_speed)

        grid_size = QHBoxLayout()
        lbl_size = QLabel("Kích thước:", self)
        lbl_size.setStyleSheet("color: #64748b; font-size: 12px;")
        grid_size.addWidget(lbl_size)
        self.combo_size = QComboBox(self)
        self.combo_size.setToolTip("Chọn kích thước output GIF")
        self.combo_size.addItems([
            "📐 Độ phân giải gốc",
            "📐 Vừa (720px)",
            "📐 Nhỏ (480px)",
            "📐 Siêu nhỏ (320px)"
        ])
        self.combo_size.setCurrentIndex(0)
        grid_size.addWidget(self.combo_size)
        simple_lay.addLayout(grid_size)

        gif_layout.addWidget(self.simple_widget)

        # 3.2 Advanced Mode Widget
        self.advanced_widget = QWidget(self)
        advanced_lay = QVBoxLayout(self.advanced_widget)
        advanced_lay.setContentsMargins(0, 0, 0, 0)
        advanced_lay.setSpacing(8)

        grid_layout4 = QHBoxLayout()
        lbl_w = QLabel("Chiều rộng (px):", self)
        lbl_w.setStyleSheet("color: #64748b; font-size: 12px;")
        grid_layout4.addWidget(lbl_w)
        self.spin_gif_w = QSpinBox(self)
        self.spin_gif_w.setRange(0, 3840)
        self.spin_gif_w.setValue(480)
        self.spin_gif_w.setSpecialValueText("Gốc")
        self.spin_gif_w.setToolTip("Chiều rộng GIF xuất ra (0 = giữ nguyên)")
        grid_layout4.addWidget(self.spin_gif_w)
        advanced_lay.addLayout(grid_layout4)

        grid_layout5 = QHBoxLayout()
        lbl_h = QLabel("Chiều cao (px):", self)
        lbl_h.setStyleSheet("color: #64748b; font-size: 12px;")
        grid_layout5.addWidget(lbl_h)
        self.spin_gif_h = QSpinBox(self)
        self.spin_gif_h.setRange(0, 2160)
        self.spin_gif_h.setValue(0)
        self.spin_gif_h.setSpecialValueText("Tự động")
        self.spin_gif_h.setToolTip("Chiều cao GIF xuất ra (0 = tự tính tỉ lệ)")
        grid_layout5.addWidget(self.spin_gif_h)
        advanced_lay.addLayout(grid_layout5)

        grid_layout6 = QHBoxLayout()
        lbl_delay = QLabel("Độ trễ (ms):", self)
        lbl_delay.setStyleSheet("color: #64748b; font-size: 12px;")
        grid_layout6.addWidget(lbl_delay)
        self.spin_delay = QSpinBox(self)
        self.spin_delay.setRange(10, 5000)
        self.spin_delay.setValue(100)
        self.spin_delay.setToolTip("Thời gian hiển thị mỗi frame (ms). Nhỏ hơn = nhanh hơn")
        self.spin_delay.valueChanged.connect(self.on_delay_changed)
        grid_layout6.addWidget(self.spin_delay)
        advanced_lay.addLayout(grid_layout6)

        grid_layout7 = QHBoxLayout()
        lbl_loop = QLabel("Số vòng lặp:", self)
        lbl_loop.setStyleSheet("color: #64748b; font-size: 12px;")
        grid_layout7.addWidget(lbl_loop)
        self.spin_loop = QSpinBox(self)
        self.spin_loop.setRange(-1, 999)
        self.spin_loop.setValue(0)
        self.spin_loop.setSpecialValueText("∞ Vô hạn")
        self.spin_loop.setToolTip("Số lần lặp lại GIF (0 = vô hạn)")
        grid_layout7.addWidget(self.spin_loop)
        advanced_lay.addLayout(grid_layout7)

        gif_layout.addWidget(self.advanced_widget)
        self.advanced_widget.setVisible(False)

        scroll_layout.addWidget(self.grp_gif)

        scroll_layout.addStretch(1)

        # ── Export Button (full width, prominent green) ────────────────────
        self.btn_export = QPushButton("  ✦  XUẤT GIF CHẤT LƯỢNG CAO", self)
        self.btn_export.setEnabled(False)
        self.btn_export.setObjectName("exportButton")
        self.btn_export.setIcon(get_svg_icon("zap", size=QSize(18, 18), color="#ffffff"))
        self.btn_export.setToolTip("Xuất GIF với chất lượng tối ưu từ các frame đã chọn")
        self.btn_export.clicked.connect(self.export_gif)
        scroll_layout.addWidget(self.btn_export)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        self.progress_bar.setTextVisible(True)
        scroll_layout.addWidget(self.progress_bar)

        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

    # --- Video Loading ---
    def browse_video(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Chọn Video", "", "Video Files (*.mp4 *.mkv *.avi *.mov *.wmv)"
        )
        if file_path:
            self.load_video_from_path(file_path)

    def load_video_from_path(self, file_path):
        if not file_path or not os.path.exists(file_path):
            return
            
        # Stop preview timer if running
        if self.preview_timer.isActive():
            self.preview_timer.stop()
            self.update_play_button_state(False)
            
        self.video_path = file_path
        fname = os.path.basename(file_path)
        self.lbl_video_path.setText(fname)
        self.lbl_video_title.setText(fname.upper()[:60] + ("..." if len(fname) > 60 else ""))
        self.drop_hint.setVisible(False)
        self.set_status(f"Đang tải thông tin: {fname}", active=True)
        
        # Clear existing frames
        self.all_frames.clear()
        self.frames_list_widget.clear()
        self.current_frame = None
        self.display_frame(None)
        self.lbl_frames_count.setText("0 frames")
        self.timeline_slider.setRange(0, 0)
        self.timeline_slider.setValue(0)
        self.grp_gif.setEnabled(False)
        self.btn_export.setEnabled(False)
        
        # Start Info Worker
        self.btn_load_video.setEnabled(False)
        self.info_worker = VideoInfoWorker(file_path)
        self.info_worker.info_ready.connect(self.on_video_info_ready)
        self.info_worker.error_occurred.connect(self.on_worker_error)
        self.info_worker.finished.connect(lambda: self.btn_load_video.setEnabled(True))
        self.info_worker.start()

    # --- Drag & Drop Events ---
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                fpath = url.toLocalFile()
                if fpath.lower().endswith(('.mp4', '.mkv', '.avi', '.mov', '.wmv')):
                    event.acceptProposedAction()
                    self.center_frame.setProperty("dragOver", "true")
                    self.center_frame.style().unpolish(self.center_frame)
                    self.center_frame.style().polish(self.center_frame)
                    return
        event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                fpath = url.toLocalFile()
                if fpath.lower().endswith(('.mp4', '.mkv', '.avi', '.mov', '.wmv')):
                    event.acceptProposedAction()
                    return
        event.ignore()

    def dragLeaveEvent(self, event):
        self.center_frame.setProperty("dragOver", "false")
        self.center_frame.style().unpolish(self.center_frame)
        self.center_frame.style().polish(self.center_frame)
        event.accept()

    def dropEvent(self, event):
        self.center_frame.setProperty("dragOver", "false")
        self.center_frame.style().unpolish(self.center_frame)
        self.center_frame.style().polish(self.center_frame)
        
        for url in event.mimeData().urls():
            fpath = url.toLocalFile()
            if fpath.lower().endswith(('.mp4', '.mkv', '.avi', '.mov', '.wmv')):
                self.load_video_from_path(fpath)
                event.acceptProposedAction()
                return
        event.ignore()

    @Slot(dict)
    def on_video_info_ready(self, info):
        self.video_info = info
        self.lbl_video_meta.setText(
            f"⏱ Thời lượng: {info['duration']:.2f}s     "
            f"📐 {info['width']}×{info['height']}     "
            f"🎞 {info['fps']:.1f} FPS"
        )
        # Configure slice parameters
        duration_sec = int(info['duration'])
        self.spin_start.setRange(0, duration_sec)
        self.spin_end.setRange(0, duration_sec + 1)
        self.spin_start.setValue(0)
        self.spin_end.setValue(min(10, duration_sec))
        
        self.grp_slice.setEnabled(True)
        self.set_status(f"Video đã tải · {info['width']}×{info['height']} · {info['fps']:.1f}FPS · {info['duration']:.1f}s", active=False)

    # --- Frame Extraction ---
    def start_frame_extraction(self):
        if not self.video_path:
            return
        
        start_sec = self.spin_start.value()
        end_sec = self.spin_end.value()
        target_fps = self.spin_fps.value()

        if end_sec <= start_sec:
            QMessageBox.warning(self, "Lỗi", "Thời gian kết thúc phải lớn hơn thời gian bắt đầu.")
            return

        # Setup progress bar
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("Trích xuất: %p%")
        
        self.btn_extract.setEnabled(False)
        self.btn_load_video.setEnabled(False)
        self.btn_export.setEnabled(False)
        
        # Stop preview timer if running
        if self.preview_timer.isActive():
            self.preview_timer.stop()
            self.update_play_button_state(False)

        # Clear existing frames
        self.all_frames.clear()
        self.frames_list_widget.clear()
        self.current_frame = None
        self.display_frame(None)
        
        # Start background Frame Extraction
        self.extract_worker = FrameExtractWorker(
            self.video_path, start_sec, end_sec, target_fps
        )
        self.extract_worker.progress.connect(self.progress_bar.setValue)
        self.extract_worker.frame_extracted.connect(self.on_frame_extracted)
        self.extract_worker.finished.connect(self.on_extraction_finished)
        self.extract_worker.error_occurred.connect(self.on_worker_error)
        self.extract_worker.start()

    @Slot(dict)
    def on_frame_extracted(self, frame_data):
        frame_data["enabled"] = True
        self.all_frames.append(frame_data)
        
        # Add item to Sidebar list
        item = QListWidgetItem(self.frames_list_widget)
        item.setSizeHint(QSize(250, 68))
        
        card = FrameCardWidget(frame_data, self)
        frame_data["card_widget"] = card
        
        self.frames_list_widget.addItem(item)
        self.frames_list_widget.setItemWidget(item, card)

        # Update stats
        count = len(self.all_frames)
        self.lbl_frames_count.setText(f"{count} frames")
        
        # Select first frame automatically
        if count == 1:
            self.display_frame(frame_data)
            self.current_preview_idx = 0
            self.timeline_slider.setRange(0, 0)
            self.timeline_slider.setValue(0)

    @Slot(list)
    def on_extraction_finished(self, frames):
        self.progress_bar.setVisible(False)
        self.btn_extract.setEnabled(True)
        self.btn_load_video.setEnabled(True)
        
        if self.all_frames:
            self.grp_gif.setEnabled(True)
            self.btn_export.setEnabled(True)
            self.timeline_slider.setRange(0, len(self.all_frames) - 1)
            self.timeline_slider.setValue(0)
            self.display_frame(self.all_frames[0])
            self.current_preview_idx = 0
            
            # Sync target dimensions
            self.spin_gif_w.setValue(self.video_info.get("width", 480))
            
            # Suggest delay based on FPS
            fps = self.spin_fps.value()
            delay_ms = int(1000 / fps) if fps > 0 else 100
            self.spin_delay.setValue(delay_ms)
            
            # Reset combos
            self.combo_speed.setCurrentIndex(0)
            self.combo_size.setCurrentIndex(0)

            n = len(self.all_frames)
            self.lbl_frames_count.setText(f"{n} frames")
            self.set_status(f"✓ Trích xuất hoàn tất · {n} frames sẵn sàng", active=False)
        else:
            self.set_status("Không trích xuất được frame nào.", active=False)
            QMessageBox.information(self, "Thông báo", "Không trích xuất được frame nào.")

    # --- Frame selection/toggling and deletion ---
    def toggle_frame(self, index, enabled):
        for f in self.all_frames:
            if f["index"] == index:
                f["enabled"] = enabled
                break

    def delete_frame(self, index):
        # Stop preview timer
        was_playing = self.preview_timer.isActive()
        if was_playing:
            self.preview_timer.stop()
            self.update_play_button_state(False)

        # Find frame
        target_idx = -1
        for i, f in enumerate(self.all_frames):
            if f["index"] == index:
                target_idx = i
                break
        
        if target_idx != -1:
            self.all_frames.pop(target_idx)
            
            # Recalculate working index indices
            for i, f in enumerate(self.all_frames):
                f["index"] = i
                if "card_widget" in f:
                    f["card_widget"].index = i
                    f["card_widget"].lbl_num.setText(f"Frame #{i + 1}")
            
            # Re-render list
            self.rebuild_frames_list()

            # Update stats and timeline slider range
            self.lbl_frames_count.setText(f"{len(self.all_frames)} frames")
            
            if not self.all_frames:
                self.btn_export.setEnabled(False)
                self.grp_gif.setEnabled(False)
                self.display_frame(None)
                self.timeline_slider.setRange(0, 0)
            else:
                self.timeline_slider.setRange(0, len(self.all_frames) - 1)
                # Ensure current_preview_idx is safe
                self.current_preview_idx = min(self.current_preview_idx, len(self.all_frames) - 1)
                self.display_frame(self.all_frames[self.current_preview_idx])
                self.timeline_slider.setValue(self.current_preview_idx)
                
                # Resume if was playing
                if was_playing:
                    self.preview_timer.start(self.spin_delay.value())
                    self.update_play_button_state(True)

    def rebuild_frames_list(self):
        self.frames_list_widget.clear()
        for frame_data in self.all_frames:
            item = QListWidgetItem(self.frames_list_widget)
            item.setSizeHint(QSize(250, 68))
            
            card = FrameCardWidget(frame_data, self)
            frame_data["card_widget"] = card
            
            # Reapply checkbox state
            card.checkbox.setChecked(frame_data["enabled"])
            card.opacity_effect.setOpacity(1.0 if frame_data["enabled"] else 0.4)
            
            self.frames_list_widget.addItem(item)
            self.frames_list_widget.setItemWidget(item, card)

    def select_all_frames(self):
        for f in self.all_frames:
            f["enabled"] = True
            if "card_widget" in f:
                f["card_widget"].checkbox.setChecked(True)

    def deselect_all_frames(self):
        for f in self.all_frames:
            f["enabled"] = False
            if "card_widget" in f:
                f["card_widget"].checkbox.setChecked(False)

    # --- Preview Panel Interactions ---
    def on_frame_item_clicked(self, item):
        row = self.frames_list_widget.row(item)
        if 0 <= row < len(self.all_frames):
            # If playing, pause first
            if self.preview_timer.isActive():
                self.preview_timer.stop()
                self.update_play_button_state(False)
            
            self.current_preview_idx = row
            self.display_frame(self.all_frames[row])
            self.timeline_slider.setValue(row)

    def display_frame(self, frame):
        if not frame:
            self.preview_label.setPixmap(QPixmap())
            self.lbl_preview_status.setText("Frame: 0/0 | Time: 0.00s")
            return
        
        self.current_frame = frame
        pix = QPixmap.fromImage(frame["preview"])
        self.preview_label.setPixmap(pix)
        
        self.lbl_preview_status.setText(
            f"Frame: {frame['index'] + 1}/{len(self.all_frames)} | "
            f"Time: {frame['timestamp']:.2f}s | "
            f"Số frame gốc: {frame['frame_num']}"
        )

    def resizeEvent(self, event):
        super().resizeEvent(event)

    # --- Timeline scrub ---
    def on_timeline_scrubbed(self, value):
        if 0 <= value < len(self.all_frames):
            # Pause play
            if self.preview_timer.isActive():
                self.preview_timer.stop()
                self.update_play_button_state(False)
            
            self.current_preview_idx = value
            self.display_frame(self.all_frames[value])
            
            # Select/scroll sidebar item to match scrubbed slider
            item = self.frames_list_widget.item(value)
            if item:
                self.frames_list_widget.setCurrentItem(item)
                self.frames_list_widget.scrollToItem(item)

    # --- Preview Playback Control ---
    def toggle_play_preview(self):
        if not self.all_frames:
            return
        
        if self.preview_timer.isActive():
            self.preview_timer.stop()
            self.update_play_button_state(False)
        else:
            delay = self.spin_delay.value()
            self.preview_timer.start(delay)
            self.update_play_button_state(True)

    def play_next_frame(self):
        active_frames = [f for f in self.all_frames if f["enabled"]]
        if not active_frames:
            return
        
        # Loop playback within active enabled frames
        self.current_preview_idx = (self.current_preview_idx + 1) % len(self.all_frames)
        
        # If the frame at current index is disabled, find the next enabled frame
        attempts = 0
        while not self.all_frames[self.current_preview_idx]["enabled"] and attempts < len(self.all_frames):
            self.current_preview_idx = (self.current_preview_idx + 1) % len(self.all_frames)
            attempts += 1
            
        frame = self.all_frames[self.current_preview_idx]
        self.display_frame(frame)
        self.timeline_slider.setValue(self.current_preview_idx)

        # Highlight sidebar item
        item = self.frames_list_widget.item(self.current_preview_idx)
        if item:
            self.frames_list_widget.setCurrentItem(item)
            self.frames_list_widget.scrollToItem(item)

    def prev_frame(self):
        if not self.all_frames:
            return
        # Pause playback
        if self.preview_timer.isActive():
            self.preview_timer.stop()
            self.update_play_button_state(False)
            
        self.current_preview_idx = (self.current_preview_idx - 1) % len(self.all_frames)
        self.display_frame(self.all_frames[self.current_preview_idx])
        self.timeline_slider.setValue(self.current_preview_idx)
        
        item = self.frames_list_widget.item(self.current_preview_idx)
        if item:
            self.frames_list_widget.setCurrentItem(item)
            self.frames_list_widget.scrollToItem(item)

    def next_frame(self):
        if not self.all_frames:
            return
        # Pause playback
        if self.preview_timer.isActive():
            self.preview_timer.stop()
            self.update_play_button_state(False)
            
        self.current_preview_idx = (self.current_preview_idx + 1) % len(self.all_frames)
        self.display_frame(self.all_frames[self.current_preview_idx])
        self.timeline_slider.setValue(self.current_preview_idx)
        
        item = self.frames_list_widget.item(self.current_preview_idx)
        if item:
            self.frames_list_widget.setCurrentItem(item)
            self.frames_list_widget.scrollToItem(item)

    def on_delay_changed(self, value):
        # Update preview timer interval if it's active
        if self.preview_timer.isActive():
            self.preview_timer.setInterval(value)

    def on_gif_mode_changed(self):
        is_simple = self.rad_simple.isChecked()
        self.simple_widget.setVisible(is_simple)
        self.advanced_widget.setVisible(not is_simple)
        if is_simple:
            self.on_simple_speed_changed()
        else:
            self.on_delay_changed(self.spin_delay.value())

    def on_simple_speed_changed(self):
        speed_multipliers = [1.0, 1.25, 1.5, 1.75, 2.0, 3.0, 0.75, 0.5, 0.25]
        idx = self.combo_speed.currentIndex()
        speed_mult = speed_multipliers[idx] if 0 <= idx < len(speed_multipliers) else 1.0
        
        slice_fps = self.spin_fps.value()
        if slice_fps <= 0:
            slice_fps = 10
            
        delay = int((1000 / slice_fps) / speed_mult)
        delay = max(10, min(delay, 5000))
        
        if self.preview_timer.isActive():
            self.preview_timer.setInterval(delay)

    # --- GIF Exporting ---
    def export_gif(self):
        # Filter selected frame numbers
        selected_frames = [f for f in self.all_frames if f["enabled"]]
        if not selected_frames:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn ít nhất 1 frame để xuất GIF.")
            return

        frame_numbers = [f["frame_num"] for f in selected_frames]
        
        # Generate output path automatically in output/ folder
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        app_root = get_app_root()
        output_dir = os.path.join(app_root, "output")
        os.makedirs(output_dir, exist_ok=True)

        if self.video_path:
            video_name = os.path.splitext(os.path.basename(self.video_path))[0]
        else:
            video_name = "kath_animation"

        output_path = os.path.join(output_dir, f"{video_name}_{timestamp}.gif")

        # Settings (Simple vs Advanced mode resolving)
        is_simple = self.rad_simple.isChecked()
        if is_simple:
            speed_multipliers = [1.0, 1.25, 1.5, 1.75, 2.0, 3.0, 0.75, 0.5, 0.25]
            idx = self.combo_speed.currentIndex()
            speed_mult = speed_multipliers[idx] if 0 <= idx < len(speed_multipliers) else 1.0
            
            slice_fps = self.spin_fps.value()
            if slice_fps <= 0:
                slice_fps = 10
                
            frame_delay = int((1000 / slice_fps) / speed_mult)
            frame_delay = max(10, min(frame_delay, 5000))
            
            size_map = [0, 720, 480, 320]
            s_idx = self.combo_size.currentIndex()
            gif_width = size_map[s_idx] if 0 <= s_idx < len(size_map) else 480
            gif_height = 0
            loop_count = 0  # Infinite
        else:
            gif_width = self.spin_gif_w.value()
            gif_height = self.spin_gif_h.value()
            frame_delay = self.spin_delay.value()
            loop_count = self.spin_loop.value()

        # Compute auto height if needed
        if gif_height == 0 and self.video_info:
            orig_w = self.video_info.get("width", 1)
            orig_h = self.video_info.get("height", 1)
            w = orig_w if gif_width == 0 else gif_width
            gif_height = int(w * (orig_h / orig_w))

        # Update UI states
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("Đang xuất GIF: %p%")
        
        self.btn_export.setEnabled(False)
        self.btn_load_video.setEnabled(False)
        self.btn_extract.setEnabled(False)

        # Threaded exporter
        self.export_worker = GifExportWorker(
            self.video_path,
            frame_numbers,
            output_path,
            gif_width,
            gif_height,
            frame_delay,
            loop_count
        )
        self.export_worker.progress.connect(self.progress_bar.setValue)
        self.export_worker.finished.connect(self.on_export_finished)
        self.export_worker.error_occurred.connect(self.on_worker_error)
        self.export_worker.start()

    @Slot(str)
    def on_export_finished(self, out_path):
        self.progress_bar.setVisible(False)
        self.btn_export.setEnabled(True)
        self.btn_load_video.setEnabled(True)
        self.btn_extract.setEnabled(True)

        fname = os.path.basename(out_path)
        self.set_status(f"✓ GIF đã xuất thành công: {fname}", active=False)

        QMessageBox.information(
            self,
            "✓ Xuất GIF Thành Công",
            f"GIF đã được lưu thành công!\n\n📁 {out_path}"
        )
        # Open containing folder
        try:
            import subprocess
            norm_path = os.path.normpath(out_path)
            subprocess.run(["explorer.exe", "/select,", norm_path], check=False)
        except Exception:
            dir_path = os.path.dirname(out_path)
            os.startfile(dir_path)

    # --- Error handler ---
    @Slot(str)
    def on_worker_error(self, err_msg):
        self.progress_bar.setVisible(False)
        self.btn_export.setEnabled(True)
        self.btn_load_video.setEnabled(True)
        self.btn_extract.setEnabled(True)
        self.set_status(f"⚠ Lỗi: {err_msg[:80]}", active=False)
        QMessageBox.critical(self, "Lỗi Hệ Thống", f"Đã xảy ra lỗi:\n{err_msg}")

    def closeEvent(self, event):
        # Stop preview timer if active
        if hasattr(self, 'preview_timer') and self.preview_timer.isActive():
            self.preview_timer.stop()
            
        # Cancel extraction worker if running
        if hasattr(self, 'extract_worker') and self.extract_worker and self.extract_worker.isRunning():
            try:
                self.extract_worker.cancel()
                self.extract_worker.terminate()
                self.extract_worker.wait()
            except Exception:
                pass

        # Terminate info worker if running
        if hasattr(self, 'info_worker') and self.info_worker and self.info_worker.isRunning():
            try:
                self.info_worker.terminate()
                self.info_worker.wait()
            except Exception:
                pass

        # Terminate export worker if running
        if hasattr(self, 'export_worker') and self.export_worker and self.export_worker.isRunning():
            try:
                self.export_worker.terminate()
                self.export_worker.wait()
            except Exception:
                pass

        # Clean exit to prevent zombie processes
        event.accept()
        import os
        os._exit(0)


def global_exception_handler(exctype, value, tb):
    """Global handler for uncaught exceptions to show dialog and prevent zombie process."""
    import traceback
    err_msg = "".join(traceback.format_exception(exctype, value, tb))
    print(err_msg, file=sys.stderr)
    try:
        from PySide6.QtWidgets import QApplication, QMessageBox
        app = QApplication.instance() or QApplication(sys.argv)
        QMessageBox.critical(
            None,
            "Lỗi Hệ Thống Nghiêm Trọng",
            f"Đã xảy ra lỗi hệ thống nghiêm trọng:\n\n{value}\n\nChi tiết lỗi:\n{err_msg}"
        )
    except Exception:
        pass
    import os
    os._exit(1)

# System-wide Mutex reference to keep it alive during the lifetime of the process
_app_mutex = None

def check_single_instance():
    global _app_mutex
    # If launched by launcher, the mutex is already held by launcher
    if os.environ.get("KATHGIFMAKER_MUTEX_HELD") == "1":
        return True

    if sys.platform == "win32":
        try:
            import ctypes
            mutex_name = "Local\\KathGifMaker_SingleInstance_Mutex"
            _app_mutex = ctypes.windll.kernel32.CreateMutexW(None, True, mutex_name)
            last_error = ctypes.windll.kernel32.GetLastError()
            if last_error == 183:  # ERROR_ALREADY_EXISTS
                if _app_mutex:
                    ctypes.windll.kernel32.CloseHandle(_app_mutex)
                    _app_mutex = None
                return False
        except Exception:
            pass
    else:
        try:
            from PySide6.QtCore import QLockFile, QDir
            lock_path = os.path.join(QDir.tempPath(), "KathGifMaker.lock")
            global _lock_file
            _lock_file = QLockFile(lock_path)
            if not _lock_file.tryLock(100):
                return False
        except Exception:
            pass
    return True

if __name__ == "__main__":
    # Register global exception handler
    sys.excepthook = global_exception_handler

    # Check if another instance is already running
    if not check_single_instance():
        app = QApplication(sys.argv)
        QMessageBox.warning(
            None,
            "Ứng Dụng Đang Chạy",
            "Ứng dụng KathGifMaker đang được chạy ở một cửa sổ khác.\n"
            "Vui lòng đóng ứng dụng đó trước khi mở lại."
        )
        sys.exit(0)

    # Ensure Windows taskbar displays the custom icon correctly in dev mode
    # In frozen (compiled EXE) mode, skipping this prevents Windows from grouping it as a separate icon.
    if not getattr(sys, 'frozen', False):
        import ctypes
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("kath.gifmaker.app.1")
        except Exception:
            pass

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

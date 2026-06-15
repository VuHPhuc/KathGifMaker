# 🎬 KathGifMaker

**KathGifMaker** là một ứng dụng desktop chuyên nghiệp giúp chuyển đổi phân đoạn từ video thành tệp ảnh động GIF chất lượng cao. Ứng dụng sở hữu giao diện tối (dark theme) hiện đại, trực quan cùng các tính năng điều khiển trích xuất frame linh hoạt.

---

## ✨ Tính Năng Nổi Bật

1. **Giao Diện Hiện Đại & Trực Quan**: Giao diện tối được tối ưu hóa hiển thị, mượt mà và tương thích tốt trên Windows.
2. **Kéo & Thả Video**: Hỗ trợ kéo và thả tệp video (`.mp4`, `.mkv`, `.avi`, `.mov`, `.wmv`) trực tiếp vào màn hình preview để tải nhanh thông tin.
3. **Trích Xuất Frame Linh Hoạt**:
   - Chọn khoảng thời gian cắt (Bắt đầu - Kết thúc).
   - Thiết lập tốc độ FPS trích xuất tùy chỉnh (hỗ trợ lên tới 120 FPS).
4. **Trình Xem Preview Tiện Lợi**: Xem trước hoạt ảnh GIF, tua từng frame hoặc phát/tạm dừng hoạt ảnh trước khi xuất bản.
5. **Cấu Hình GIF Chuyên Sâu**:
   - **Chế độ Cơ Bản**: Lựa chọn nhanh Tốc độ phát (0.25x đến 3.0x) và Kích thước đầu ra (320px, 480px, 720px hoặc Giữ nguyên gốc).
   - **Chế độ Nâng Cao**: Cho phép thay đổi độ rộng/cao tùy ý, cấu hình độ trễ (delay) chi tiết đến mili-giây và thiết lập số vòng lặp (loop count).
6. **Vận Hành Ổn Định & An Toàn**:
   - **Chặn chạy trùng bản sao (Single Instance)**: Tự động phát hiện và ngăn chặn người dùng bật nhiều bản sao cùng lúc để bảo vệ tài nguyên phần cứng.
   - **Chống Tiến Trình Zombie**: Xử lý ngoại lệ toàn cục hiển thị hộp thoại lỗi chi tiết và tự dọn dẹp các tiến trình chạy ngầm (`QThread`) khi tắt ứng dụng, đảm bảo không bị kẹt tiến trình ngầm trong Task Manager.

---

## 🛠️ Yêu Cầu Hệ Thống & Cài Đặt

Ứng dụng được viết bằng **Python** và **PySide6** (Qt for Python).

### Cách Chạy từ Mã Nguồn (Development Mode)

1. Cài đặt Python 3.10+ trên máy tính của bạn.
2. Mở terminal tại thư mục dự án và khởi tạo môi trường ảo:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
3. Cài đặt các thư viện phụ thuộc:
   ```bash
   pip install -r requirements.txt
   ```
4. Khởi chạy ứng dụng:
   ```bash
   python src/launcher.py
   ```

---

## 📦 Đóng Gói Ứng Dụng Thành File `.exe`

Ứng dụng đi kèm sẵn script hỗ trợ đóng gói nhanh bằng **PyInstaller** thành một file chạy duy nhất trên Windows:

```bash
python src/build_exe.py
```

Sau khi đóng gói thành công:
- File thực thi `KathGifMaker.exe` sẽ được tạo và sao chép ra thư mục gốc dự án.
- Bạn có thể phân phối và chạy trực tiếp file này trên bất kỳ máy Windows nào mà không cần cài đặt Python.

---

## 📂 Cấu Trúc Thư Mục Dự Án

```text
KathGifMaker/
├── src/
│   ├── app_icon.ico       # Icon ứng dụng
│   ├── build_exe.py       # Script đóng gói thành .exe
│   ├── icons.py           # Module nạp SVG icons đẹp mắt
│   ├── launcher.py        # Điểm bắt đầu (Launcher) xử lý Single Instance
│   ├── main.py            # Logic giao diện chính PySide6 & excepthook dọn dẹp
│   ├── styles.py          # Stylesheet QSS giao diện tối hiện đại
│   └── video_processor.py # Luồng trích xuất và xuất GIF ngầm (QThread, OpenCV, PIL)
├── KathGifMaker.exe       # Bản phân phối chạy độc lập (sau khi build)
├── requirements.txt       # Danh sách thư viện cần thiết
└── README.md              # Tài liệu hướng dẫn sử dụng
```

---

## 📝 Bản Quyền

Được phát triển với tình yêu bởi **Kath**. Hỗ trợ định dạng và tạo GIF chất lượng cao tối ưu hóa cho mạng xã hội và các nền tảng chia sẻ trực tuyến.

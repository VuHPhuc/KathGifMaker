# src/launcher.py
import os
import sys
import traceback

# Placeholder imports for PyInstaller static analysis so they get bundled inside the EXE
if False:
    import PySide6.QtWidgets
    import PySide6.QtCore
    import PySide6.QtGui
    import PySide6.QtSvg
    import cv2
    import PIL.Image
    import PIL.ImageFilter
    import numpy

def main():
    # Find directory where the executable (or script) is located
    if getattr(sys, 'frozen', False):
        # Running as compiled EXE (which sits in the root folder)
        app_root = os.path.dirname(sys.executable)
        local_src = os.path.join(app_root, "src")
    else:
        # Running as python src/launcher.py
        launcher_dir = os.path.dirname(os.path.abspath(__file__))  # this is '<root>/src'
        local_src = launcher_dir
        app_root = os.path.dirname(local_src)  # this is the root folder

    # Configure sys.path so imports resolve to the local 'src' folder first
    if local_src not in sys.path:
        sys.path.insert(0, local_src)
    
    # Keep working directory as the workspace root so output/ and venv/ paths resolve naturally
    os.chdir(app_root)

    local_main = os.path.join(local_src, "main.py")

    if os.path.exists(local_main):
        try:
            # Read and execute main.py dynamically
            with open(local_main, "r", encoding="utf-8") as f:
                code_content = f.read()

            # Set up correct namespace environment
            globals_dict = {
                "__file__": local_main,
                "__name__": "__main__",
                "__package__": None
            }
            exec(code_content, globals_dict)
        except Exception as e:
            # Show visual graphical error dialog if runtime errors occur
            from PySide6.QtWidgets import QApplication, QMessageBox
            app = QApplication.instance() or QApplication(sys.argv)
            QMessageBox.critical(
                None,
                "Lỗi Runtime main.py",
                f"Đã xảy ra lỗi khi thực thi mã nguồn local main.py:\n\n{traceback.format_exc()}"
            )
    else:
        from PySide6.QtWidgets import QApplication, QMessageBox
        app = QApplication.instance() or QApplication(sys.argv)
        QMessageBox.critical(
            None,
            "Không Tìm Thấy File",
            f"Không tìm thấy file mã nguồn 'main.py' tại đường dẫn:\n{local_main}\n\n"
            "Hãy đảm bảo thư mục 'src' chứa 'main.py' nằm cùng cấp với file chạy .exe."
        )

if __name__ == "__main__":
    main()

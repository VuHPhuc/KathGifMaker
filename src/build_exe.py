# src/build_exe.py
import os
import sys
import subprocess
import shutil

def build():
    print("=== START PACKAGING KATHGIFMAKER TO EXE ===")
    
    # Set working directory to workspace root (parent of 'src')
    script_dir = os.path.dirname(os.path.abspath(__file__))  # this is '<root>/src'
    root_dir = os.path.dirname(script_dir)  # this is '<root>'
    os.chdir(root_dir)
    print(f"Working directory set to: {os.getcwd()}")
    
    # Path to virtual environment's pyinstaller
    venv_pyinstaller = os.path.join("venv", "Scripts", "pyinstaller.exe")
    if not os.path.exists(venv_pyinstaller):
        # Fallback to standard pyinstaller in path
        venv_pyinstaller = "pyinstaller"
        print("Pyinstaller not found in venv. Using system default pyinstaller.")

    # PyInstaller arguments
    cmd = [
        venv_pyinstaller,
        "--onefile",
        "--windowed",
        "--name=KathGifMaker",
        "--clean",
        "--icon=src/app_icon.ico",
        "--add-data=src/app_icon.ico;.",
        os.path.join("src", "launcher.py")
    ]

    print(f"Running command: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, check=True)
        if result.returncode == 0:
            print("\n=== PACKAGING SUCCESSFUL! ===")
            print("EXE is located in 'dist/KathGifMaker.exe'")
            
            # Copy to workspace root
            root_exe = "KathGifMaker.exe"
            try:
                shutil.copy2(os.path.join("dist", "KathGifMaker.exe"), root_exe)
                print(f"Copied executable to workspace root: '{root_exe}'")
            except Exception as copy_err:
                print(f"Warning: Could not copy executable to root: {copy_err}")
                
            print("You can copy this file to any Windows machine and run it.")
        else:
            print(f"\nPackaging failed with exit code: {result.returncode}")
    except subprocess.CalledProcessError as e:
        print(f"\nError executing PyInstaller: {e}")
    except Exception as e:
        print(f"\nUnexpected error occurred: {e}")

if __name__ == "__main__":
    build()

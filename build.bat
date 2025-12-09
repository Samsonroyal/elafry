@echo off
rem Convert PNG to ICO for the executable icon
rem Note: PyInstaller can use PNG but ICO is better for Windows. 
rem For simplicity we will try pointing to PNG, if it fails we might need a converter. 
rem Windows often accepts PNG for window icons but the exe icon usually needs .ico. 
rem Since we don't have an easy converter, we will use the PNG and see if PyInstaller complains or just handles it (modern versions often do).
rem Actually, to be safe, let's just use the PNG as a data file and set the window icon in code (already done). 
rem For the EXE icon, if we don't have an .ico, we will skip the --icon flag for the visual EXE file, but the app window will still have it.

echo Building Elafrý...
rmdir /s /q dist
rmdir /s /q build
.\venv\Scripts\pyinstaller --noconfirm --onedir --windowed --name "Elafry" --add-data "logo.png;." browser.py
echo Build Complete.

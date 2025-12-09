import PyInstaller.__main__
import sys
import os
import shutil

def build():
    # Determine separator for add-data
    if sys.platform == 'win32':
        separator = ';'
        # Convert png to ico if needed
        if os.path.exists('logo.png') and not os.path.exists('logo.ico'):
            print("Converting logo.png to logo.ico...")
            try:
                from PIL import Image
                img = Image.open('logo.png')
                img.save('logo.ico', format='ICO', sizes=[(256, 256)])
                print("Conversion successful.")
            except ImportError:
                print("Pillow not installed, skipping icon conversion. Install Pillow for icon support.")
    else:
        separator = ':'

    # Basic arguments
    args = [
        'browser.py',
        '--name=Elafrý',
        '--windowed',         # No console window
        '--onefile',          # Single executable
        '--clean',
        f'--add-data=logo.png{separator}.',
        '--hidden-import=PyQt6.sip',
        '--hidden-import=PyQt6.QtCore',
        '--hidden-import=PyQt6.QtGui',
        '--hidden-import=PyQt6.QtWidgets',
        '--hidden-import=PyQt6.QtWebEngineWidgets',
        '--collect-all=PyQt6',
        '--collect-all=PyQt6-WebEngine',
    ]

    # Icon handling
    if sys.platform == 'win32':
        args.append('--icon=logo.png')
    elif sys.platform == 'darwin':
        # On Mac, we'd ideally want an .icns file, but PyInstaller might warn/skip if png is passed.
        # We'll pass it and see.
        args.append('--icon=logo.png') 
        # Enable high-res display on Mac
        args.append('--osx-bundle-identifier=com.samsonroyal.elafry')

    print(f"Building for {sys.platform}...")
    
    # Run PyInstaller
    PyInstaller.__main__.run(args)

    print("Build complete.")
    
    # Print dist location
    dist_dir = os.path.join(os.getcwd(), 'dist')
    print(f"Executable can be found in: {dist_dir}")

if __name__ == "__main__":
    build()

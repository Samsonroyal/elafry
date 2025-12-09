# Elafrý Browser

**Elafrý** (Greek for "Light") is a modern, lightweight, privacy-focused web browser for Windows built with Python and PyQt6.

![Logo](logo.png)

## Features

- **Lightweight & Fast**: Powered by QtWebEngine (Chromium).
- **Privacy First**: DuckDuckGo as the default search engine.
- **Modern UI**: Clean design with Dark and Light mode support.
- **Customizable**: Toggle themes instantly.

## Installation

### From Source

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/elafry.git
   cd elafry
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the browser:
   ```bash
   python browser.py
   ```

### Building the Executable

To create a standalone Windows executable:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```
2. Run the build script:
   ```bash
   build.bat
   ```
3. The application will be found in `dist/Elafry/Elafry.exe`.

## License

MIT License. Free and Open Source.

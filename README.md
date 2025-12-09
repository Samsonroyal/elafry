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

You can build a standalone executable for your current platform (Windows, macOS, or Linux).

1. Ensure dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the build script:
   ```bash
   python build_binaries.py
   ```
3. The executable will be found in the `dist` folder (e.g., `dist/Elafrý.exe` on Windows).

> **Note:** On Windows, the script will automatically convert `logo.png` to `logo.ico` if you have `Pillow` installed.

### Cross-Platform Automated Builds

This project includes a **GitHub Actions** workflow that automatically builds binaries for Windows, macOS, and Linux whenever you push changes or create a release. 
Check the **Actions** tab or **Releases** page on GitHub to download the latest builds.

## License

MIT License. Free and Open Source.

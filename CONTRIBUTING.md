# Contributing to Elafrý

First off, thank you for considering contributing to Elafrý! It's people like you that make the open-source community such an amazing place to learn, inspire, and create.

## Getting Started

### Prerequisites
- **Python 3.9+**: Ensure you have a modern version of Python installed.
- **Git**: To clone and manage source commands.

### Installation

1. **Fork the repository**
   - Click the "Fork" button at the top right of the GitHub page.

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/elafry.git
   cd elafry
   ```

3. **Set up a Virtual Environment** (Recommended)
   - Windows:
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - MacOS/Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Development Workflow

1. **Create a Branch**
   - Create a specific branch for your feature or fix.
   ```bash
   git checkout -b feature/amazing-feature
   ```

2. **Make your changes**
   - The main logic is located in `browser.py`.
   - If you add new dependencies, remember to update `requirements.txt`.

3. **Test your code**
   - Run the browser locally to ensure everything works as expected.
   ```bash
   python browser.py
   ```

4. **Code Style**
   - We follow standard Python **PEP 8** guidelines.
   - Try to keep the code readable and well-commented.

## Submitting a Pull Request

1. Push your changes to your fork:
   ```bash
   git push origin feature/amazing-feature
   ```
2. Go to the original Elafrý repository and click **"New Pull Request"**.
3. Describe your changes clearly.
4. Wait for review!

## Reporting Bugs

- Use the GitHub Issues tab.
- clearly describe the issue, including steps to reproduce.
- Include information about your OS and Python version.

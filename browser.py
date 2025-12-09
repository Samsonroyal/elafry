import sys
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import (QApplication, QMainWindow, QToolBar, QLineEdit, 
                             QTabWidget, QWidget, QVBoxLayout, QStatusBar)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtGui import QAction, QIcon


class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Elafrý")
        self.setWindowIcon(QIcon("logo.png"))
        self.resize(1200, 800)
        self.current_theme = "light"  # Default theme
        
        # Search Engines
        self.search_engines = {
            "DuckDuckGo": "https://duckduckgo.com/?q=",
            "Ecosia": "https://www.ecosia.org/search?q=",
            "Brave": "https://search.brave.com/search?q=",
            "Google": "https://www.google.com/search?q="
        }
        self.current_search_engine = "DuckDuckGo" # Default to a privacy-focused one

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        # Prevent initial crash if no tab styles set, will apply theme shortly
        
        # Central Widget Container
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Toolbar Container (to hold nav + url)
        self.toolbar_area = QWidget()
        self.toolbar_layout = QVBoxLayout()
        self.toolbar_layout.setContentsMargins(0, 0, 0, 0)
        self.toolbar_layout.setSpacing(0)
        self.toolbar_area.setLayout(self.toolbar_layout)

        # --- Tabs Area ---
        # We put tabs at the top level
        layout.addWidget(self.toolbar_area)
        layout.addWidget(self.tabs)

        # --- Custom Toolbar ---
        self.navbar = QToolBar()
        self.navbar.setMovable(False)
        self.navbar.setFloatable(False)
        self.toolbar_layout.addWidget(self.navbar)

        # Back
        back_btn = QAction('Back', self) # Icon placeholder: <
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        self.navbar.addAction(back_btn)

        # Forward
        forward_btn = QAction('Forward', self) # Icon placeholder: >
        forward_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        self.navbar.addAction(forward_btn)

        # Reload
        reload_btn = QAction('Refresh', self) # Icon placeholder: R
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        self.navbar.addAction(reload_btn)

        # URL Bar
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Search Google or type a URL")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.navbar.addWidget(self.url_bar)

        # Search Engine Selection
        self.search_engine_btn = QAction('Search: DDG', self)
        self.search_engine_btn.triggered.connect(self.cycle_search_engine)
        self.navbar.addAction(self.search_engine_btn)

        # Toggle Theme
        self.theme_btn = QAction('Toggle Theme', self)
        self.theme_btn.triggered.connect(self.toggle_theme)
        self.navbar.addAction(self.theme_btn)

        # Status Bar
        self.status = QStatusBar()
        self.setStatusBar(self.status)

        # Open Initialization Tab
        self.add_new_tab(QUrl('https://duckduckgo.com'), 'New Tab')

        # Apply Initial Theme
        self.apply_theme()

    def cycle_search_engine(self):
        engines = list(self.search_engines.keys())
        current_index = engines.index(self.current_search_engine)
        next_index = (current_index + 1) % len(engines)
        self.current_search_engine = engines[next_index]
        self.search_engine_btn.setText(f"Search: {self.current_search_engine}")

    def toggle_theme(self):
        if self.current_theme == "light":
            self.current_theme = "dark"
        else:
            self.current_theme = "light"
        self.apply_theme()

    def apply_theme(self):
        if self.current_theme == "dark":
            # Dark Mode Styles match Image 1
            bg_color = "#202124"
            fg_color = "#E8EAED"
            toolbar_bg = "#35363A"
            url_bg = "#202124"
            tab_bg = "#35363A"
            tab_selected = "#202124"
            tab_text = "#9AA0A6"
            
            style = f"""
            QMainWindow {{ background-color: {bg_color}; color: {fg_color}; }}
            QTabWidget::pane {{ border: 0; background: {bg_color}; }}
            QTabBar::tab {{ 
                background: {tab_bg}; 
                color: {tab_text}; 
                padding: 8px 16px; 
                border-top-left-radius: 8px; 
                border-top-right-radius: 8px; 
                margin-right: 2px;
                border: none;
            }}
            QTabBar::tab:selected {{ 
                background: {tab_selected}; 
                color: {fg_color}; 
            }}
            QToolBar {{ 
                background: {toolbar_bg}; 
                border: none; 
                padding: 5px; 
            }}
            QLineEdit {{ 
                background-color: {url_bg}; 
                color: {fg_color}; 
                border-radius: 14px; 
                padding: 6px 12px; 
                border: 1px solid #5F6368; 
                selection-background-color: #8AB4F8;
            }}
            QStatusBar {{ background: {toolbar_bg}; color: {fg_color}; }}
            """
        else:
            # Light Mode Styles match Image 2
            bg_color = "#FFFFFF"
            fg_color = "#202124"
            toolbar_bg = "#F1F3F4" # Slightly lighter gray for better refresh feel
            url_bg = "#FFFFFF"
            tab_bg = "#E8EAED"
            tab_selected = "#FFFFFF"
            tab_text = "#3c4043" # Darker gray for better contrast
            
            # Explicitly set color for tool buttons if possible via QToolButton
            style = f"""
            QMainWindow {{ background-color: {bg_color}; color: {fg_color}; }}
            QTabWidget::pane {{ border: 0; background: {bg_color}; }}
            QTabBar::tab {{ 
                background: {tab_bg}; 
                color: {tab_text}; 
                padding: 8px 16px; 
                border-top-left-radius: 8px; 
                border-top-right-radius: 8px; 
                margin-right: 2px;
                border: none;
            }}
            QTabBar::tab:selected {{ 
                background: {tab_selected}; 
                color: {fg_color}; 
                font-weight: bold;
            }}
            QToolBar {{ 
                background: {toolbar_bg}; 
                border: none; 
                padding: 5px; 
                color: {fg_color};
            }}
            QToolButton {{
                color: {fg_color};
            }}
            QLineEdit {{ 
                background-color: {url_bg}; 
                color: {fg_color}; 
                border-radius: 14px; 
                padding: 6px 12px; 
                border: none;
            }}
            QStatusBar {{ background: {toolbar_bg}; color: {fg_color}; }}
            """
        
        self.setStyleSheet(style)

    def add_new_tab(self, qurl=None, label="Blank"):
        if qurl is None:
            qurl = QUrl('https://duckduckgo.com')

        browser = QWebEngineView()
        browser.setUrl(qurl)
        
        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_url_bar(qurl, browser))

        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_tab_title(browser))
        browser.loadFinished.connect(lambda _, browser=browser: self.update_tab_title(browser))


    def tab_open_doubleclick(self, i):
        if i == -1: # Clicked on empty space
            self.add_new_tab()

    def current_tab_changed(self, i):
        if self.tabs.count() > 0:
            qurl = self.tabs.currentWidget().url()
            self.update_url_bar(qurl, self.tabs.currentWidget())
            self.update_title(self.tabs.currentWidget())

    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return
        
        self.tabs.removeTab(i)

    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            return
        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle(f"{title} - Elafrý")

    def update_tab_title(self, browser):
        index = self.tabs.indexOf(browser)
        if index >= 0:
            title = browser.page().title()
            if len(title) > 20:
                title = title[:20] + "..."
            self.tabs.setTabText(index, title)
        
        if browser == self.tabs.currentWidget():
            self.update_title(browser)

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("https://duckduckgo.com"))

    def navigate_to_url(self):
        text = self.url_bar.text()
        if not text:
            return
            
        q = QUrl(text)
        if q.scheme() == "" and "." in text:
             q.setScheme("http")
             self.tabs.currentWidget().setUrl(q)
        elif q.scheme() == "" and "." not in text:
            # Search
            search_url = self.search_engines[self.current_search_engine] + text
            self.tabs.currentWidget().setUrl(QUrl(search_url))
        else:
            self.tabs.currentWidget().setUrl(q)

    def update_url_bar(self, q, browser=None):
        if browser != self.tabs.currentWidget():
            return
        self.url_bar.setText(q.toString())
        self.url_bar.setCursorPosition(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Elafrý")
    window = BrowserWindow()
    window.show()
    sys.exit(app.exec())

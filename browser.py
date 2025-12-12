import sys
import base64
from io import BytesIO
from PyQt6.QtCore import QUrl, Qt, QSize, QTimer, QByteArray
from PyQt6.QtWidgets import (QApplication, QMainWindow, QToolBar, QLineEdit,
                             QTabWidget, QWidget, QVBoxLayout, QStatusBar,
                             QProgressBar, QSplitter, QMenu, QToolButton,
                             QSizePolicy)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings, QWebEnginePage, QWebEngineProfile
from PyQt6.QtGui import QAction, QIcon, QKeySequence, QShortcut, QPixmap, QPainter, QColor, QPen

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Elafrý")
        self.setWindowIcon(QIcon("logo.png"))
        self.resize(1200, 800)
        self.current_theme = "light"

        # Web engine settings (JavaScript enabled by default in PyQt6)
        # DevTools accessible via right-click context menu

        # Search Engines
        self.search_engines = {
            "DuckDuckGo": "https://duckduckgo.com/?q=",
            "Google": "https://www.google.com/search?q=",
            "Bing": "https://www.bing.com/search?q=",
            "Ecosia": "https://www.ecosia.org/search?q=",
        }
        self.current_search_engine = "DuckDuckGo"

        # Central Widget & Main Layout
        central_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

        # Toolbar Container
        self.toolbar_area = QWidget()
        self.toolbar_layout = QVBoxLayout()
        self.toolbar_layout.setContentsMargins(0, 0, 0, 0)
        self.toolbar_layout.setSpacing(0)
        self.toolbar_area.setLayout(self.toolbar_layout)
        self.main_layout.addWidget(self.toolbar_area)

        # 1. Navigation Toolbar (Top)
        self.navbar = QToolBar()
        self.navbar.setMovable(False)
        self.navbar.setFloatable(False)
        self.toolbar_layout.addWidget(self.navbar)

        # Lucide SVG Icons
        self.lucide_icons = {
            'chevron-left': '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg>''',
            'chevron-right': '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>''',
            'rotate-cw': '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 1 1-9-9c2.52 0 4.93 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/></svg>''',
            'home': '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>''',
        }

        # Navigation Actions with SVG Icons
        # Store actions for theme updates
        self.nav_back_action = self.add_nav_action_svg('chevron-left', self.navigate_back, "Back (Alt+Left)")
        self.nav_forward_action = self.add_nav_action_svg('chevron-right', self.navigate_forward, "Forward (Alt+Right)")
        self.nav_reload_action = self.add_nav_action_svg('rotate-cw', self.navigate_reload, "Reload (F5)")
        self.nav_home_action = self.add_nav_action_svg('home', self.navigate_home, "Home")
        
        
        # Add spacing
        self.navbar.addSeparator()

        # URL Bar
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("🔍 Search or enter URL")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_bar.setMinimumWidth(400)
        self.navbar.addWidget(self.url_bar)

        # Search Engine Cycle
        self.search_engine_btn = QAction(f'🔎 {self.current_search_engine}', self)
        self.search_engine_btn.setToolTip("Change search engine")
        self.search_engine_btn.triggered.connect(self.cycle_search_engine)
        self.navbar.addAction(self.search_engine_btn)

        # Theme Toggle
        self.theme_btn = QAction('◐', self)
        self.theme_btn.setToolTip("Toggle Dark/Light Theme")
        self.theme_btn.triggered.connect(self.toggle_theme)
        self.navbar.addAction(self.theme_btn)
        
        # New Tab Button
        new_tab_btn = QAction('+', self)
        new_tab_btn.setToolTip("New Tab (Ctrl+T)")
        new_tab_btn.triggered.connect(self.add_new_tab)
        self.navbar.addAction(new_tab_btn)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.main_layout.addWidget(self.tabs)

        # Status Bar
        self.status = QStatusBar()
        self.setStatusBar(self.status)

        # Keyboard Shortcuts
        self.shortcut_new_tab = QShortcut(QKeySequence("Ctrl+T"), self)
        self.shortcut_new_tab.activated.connect(self.add_new_tab)
        
        self.shortcut_close_tab = QShortcut(QKeySequence("Ctrl+W"), self)
        self.shortcut_close_tab.activated.connect(lambda: self.close_current_tab(self.tabs.currentIndex()))

        self.shortcut_reload = QShortcut(QKeySequence("F5"), self)
        self.shortcut_reload.activated.connect(self.navigate_reload)
        
        self.shortcut_devtools = QShortcut(QKeySequence("F12"), self)
        self.shortcut_devtools.activated.connect(lambda: self.tabs.currentWidget().page().triggerAction(QWebEnginePage.WebAction.InspectElement) if self.tabs.count() > 0 and isinstance(self.tabs.currentWidget(), QWebEngineView) else None)

        # Initialize
        self.add_new_tab(QUrl('https://duckduckgo.com'), 'New Tab')
        self.apply_theme()
        
        # Add the "+" tab
        self.update_plus_tab()

    def create_svg_icon(self, icon_name, color="#000000"):
        """Create a QIcon by drawing the icon shape"""
        pixmap = QPixmap(24, 24)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        pen = QPen(QColor(color))
        pen.setWidth(2)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        
        # Draw based on icon name
        if icon_name == 'chevron-left':
            # Draw left chevron
            painter.drawLine(15, 6, 9, 12)
            painter.drawLine(9, 12, 15, 18)
        elif icon_name == 'chevron-right':
            # Draw right chevron
            painter.drawLine(9, 6, 15, 12)
            painter.drawLine(15, 12, 9, 18)
        elif icon_name == 'rotate-cw':
            # Draw reload/refresh icon
            painter.drawArc(4, 4, 16, 16, 90 * 16, 270 * 16)
            # Arrow head
            painter.drawLine(20, 4, 20, 9)
            painter.drawLine(20, 4, 15, 4)
        elif icon_name == 'home':
            # Draw home icon
            painter.drawLine(12, 5, 4, 11)
            painter.drawLine(12, 5, 20, 11)
            painter.drawLine(4, 11, 4, 20)
            painter.drawLine(20, 11, 20, 20)
            painter.drawLine(4, 20, 20, 20)
            painter.drawLine(9, 14, 9, 20)
            painter.drawLine(15, 14, 15, 20)
            painter.drawLine(9, 14, 15, 14)
        
        painter.end()
        return QIcon(pixmap)

    def add_nav_action_svg(self, icon_name, slot, tooltip):
        """Add a navigation action with a drawn icon"""
        color = "#1F2937" if self.current_theme == "light" else "#FFFFFF"
        icon = self.create_svg_icon(icon_name, color)
        action = QAction(self)
        action.setIcon(icon)
        action.setToolTip(tooltip)
        action.triggered.connect(slot)
        self.navbar.addAction(action)
        return action

    def add_nav_action(self, icon, slot, tooltip):
        action = QAction(icon, self)
        action.setToolTip(tooltip)
        action.triggered.connect(slot)
        self.navbar.addAction(action)

    def add_sidebar_action(self, icon, slot, tooltip):
        action = QAction(icon, self)
        action.setToolTip(tooltip)
        action.triggered.connect(slot)
        self.sidebar.addAction(action)

    def add_new_tab(self, qurl=None, label="New Tab"):
        if not isinstance(qurl, QUrl):
             qurl = QUrl('https://duckduckgo.com')

        browser = self.create_browser(qurl)

        # Insert before the "+" tab if it exists
        count = self.tabs.count()
        index = count - 1 if count > 0 and self.tabs.tabText(count-1) == "+" else count
        
        i = self.tabs.insertTab(index, browser, label)
        self.tabs.setCurrentIndex(i)
        
        browser.setFocus()
        return browser

    def create_browser(self, qurl):
        browser = QWebEngineView()
        browser.setUrl(qurl)
        browser.urlChanged.connect(lambda q, b=browser: self.update_url_bar(q, b))
        browser.titleChanged.connect(lambda t, b=browser: self.update_tab_title(b, t))
        browser.page().linkHovered.connect(lambda l: self.status.showMessage(l))
        return browser



    def update_plus_tab(self):
        # Check if last tab is +, if not add it
        count = self.tabs.count()
        if count == 0 or self.tabs.tabText(count-1) != "+":
            self.tabs.addTab(QWidget(), "+")
            # We don't want the + tab to be closing-enabled usually, but QTabWidget sets it per tab via a workaround or globally.
            # Simpler to just let it be.

    def current_tab_changed(self, i):
        if i == -1: return
        
        # Check if it's the plus tab
        if self.tabs.tabText(i) == "+":
            # Create new tab and switch to it
            self.add_new_tab()
            return

        # Update URL bar
        browser = self.tabs.widget(i)
        if isinstance(browser, QWebEngineView):
            self.update_url_bar(browser.url(), browser)
            self.update_title(browser)

    def close_current_tab(self, i):
        if self.tabs.tabText(i) == "+":
            return # Don't close the plus tab
            
        if self.tabs.count() < 2: # Don't close last actual tab (excluding +)?
             # If only tab and +, close tab makes 0 tabs then we hit + logic?
             # Let's simple check:
             pass

        self.tabs.removeTab(i)
        
        # If we removed the last content tab and only + remains
        if self.tabs.count() == 1 and self.tabs.tabText(0) == "+":
             self.add_new_tab() # Keep at least one tab open

    def tab_open_doubleclick(self, i):
        if i == -1:
            self.add_new_tab()

    def update_tab_title(self, browser, title):
        # Find which tab contains this browser
        for i in range(self.tabs.count()):
            widget = self.tabs.widget(i)
            if widget == browser:
                short_title = (title[:15] + '..') if len(title) > 15 else title
                self.tabs.setTabText(i, short_title)
                if i == self.tabs.currentIndex():
                    self.setWindowTitle(f"{title} - Elafrý")
                return

    def update_title(self, browser):
        self.setWindowTitle(f"{browser.title()} - Elafrý")

    def navigate_back(self):
        self.active_browser().back()

    def navigate_forward(self):
        self.active_browser().forward()

    def navigate_reload(self):
        self.active_browser().reload()

    def navigate_home(self):
        self.active_browser().setUrl(QUrl("https://duckduckgo.com"))

    def active_browser(self):
        return self.tabs.currentWidget()

    def navigate_to_url(self):
        text = self.url_bar.text()
        if not text: return
        q = QUrl(text)
        if q.scheme() == "" and "." in text:
             q.setScheme("http")
        elif q.scheme() == "":
            q = QUrl(self.search_engines[self.current_search_engine] + text)
        
        self.active_browser().setUrl(q)

    def update_url_bar(self, q, browser):
        # Update only if it's the current tab's browser
        if self.tabs.currentWidget() == browser:
            self.url_bar.setText(q.toString())
            self.url_bar.setCursorPosition(0)

    def cycle_search_engine(self):
        engines = list(self.search_engines.keys())
        idx = engines.index(self.current_search_engine)
        self.current_search_engine = engines[(idx + 1) % len(engines)]
        self.search_engine_btn.setText(f"🔎 {self.current_search_engine}")

    def toggle_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme()

    def apply_theme(self):
        # Refresh navigation icons with new theme colors
        color = "#1F2937" if self.current_theme == "light" else "#FFFFFF"
        
        # Update navigation action icons
        if hasattr(self, 'nav_back_action'):
            self.nav_back_action.setIcon(self.create_svg_icon('chevron-left', color))
            self.nav_forward_action.setIcon(self.create_svg_icon('chevron-right', color))
            self.nav_reload_action.setIcon(self.create_svg_icon('rotate-cw', color))
            self.nav_home_action.setIcon(self.create_svg_icon('home', color))
        
        # Modern Glassmorphism-inspired Palette
        if self.current_theme == "dark":
            bg = "#1E1E1E" # Deep Gray
            fg = "#FFFFFF"
            glass_bg = "#2D2D2D" # Slightly lighter
            accent = "#61AFEF" # OneDark Blue
            border = "#3e4451"
            hover_bg = "#3a3f4b"
        else:
            bg = "#F3F4F6"
            fg = "#1F2937"
            glass_bg = "#FFFFFF"
            accent = "#0F62FE" # Enterprise Blue
            border = "#D1D5DB"
            hover_bg = "#E5E7EB"

        style = f"""
        QMainWindow {{ 
            background-color: {bg}; 
            color: {fg}; 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }}
        
        /* Navigation Bar */
        QToolBar {{
            background: {glass_bg};
            border: none;
            border-bottom: 1px solid {border};
            padding: 4px 8px;
            spacing: 4px;
        }}
        
        QToolBar QToolButton {{
            background: transparent;
            border: none;
            border-radius: 12px;
            padding: 6px;
            color: {fg};
            min-width: 32px;
            min-height: 32px;
            max-width: 32px;
            max-height: 32px;
        }}
        
        QToolBar QToolButton:hover {{
            background: {hover_bg};
        }}
        
        QToolBar QToolButton:pressed {{
            background: {accent}33;
        }}
        
        QToolBar::separator {{
            background: {border};
            width: 1px;
            margin: 6px 8px;
        }}
        
        /* URL Bar */
        QLineEdit {{
            background-color: {bg};
            color: {fg};
            border: 2px solid {border};
            border-radius: 20px;
            padding: 8px 16px;
            font-size: 14px;
            selection-background-color: {accent};
        }}
        
        QLineEdit:focus {{
            border: 2px solid {accent};
            background-color: {glass_bg};
        }}
        
        /* Tabs */
        QTabWidget::pane {{ 
            border: none; 
            background: {glass_bg}; 
        }}
        
        QTabBar::tab {{
            background: {bg};
            color: {fg};
            padding: 10px 24px;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
            border: none;
            margin-right: 2px;
            min-width: 120px;
            max-width: 200px;
        }}
        
        QTabBar::tab:selected {{
            background: {glass_bg};
            border-bottom: 3px solid {accent};
            font-weight: 600;
        }}
        
        QTabBar::tab:hover:!selected {{
            background: {hover_bg};
        }}
        
        /* Vertical Tabs Style overrides */
        QTabBar::tab:left {{
            padding: 12px 16px;
            border-top-left-radius: 10px;
            border-bottom-left-radius: 10px;
            border-top-right-radius: 0px;
            border-bottom-right-radius: 0px;
            margin-bottom: 2px;
            min-height: 48px;
        }}
        
        QTabBar::tab:left:selected {{
            border-bottom: none;
            border-right: 3px solid {accent};
        }}
        
        /* Status Bar */
        QStatusBar {{
            background: {glass_bg};
            color: {fg};
            border-top: 1px solid {border};
        }}
        
        /* Scrollbars (Modern Slim) */
        QScrollBar:vertical {{
            border: none;
            background: {bg};
            width: 8px;
            margin: 0px;
        }}
        
        QScrollBar::handle:vertical {{
            background: {border};
            min-height: 20px;
            border-radius: 4px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background: {accent};
        }}
        
        QScrollBar:horizontal {{
            border: none;
            background: {bg};
            height: 8px;
            margin: 0px;
        }}
        
        QScrollBar::handle:horizontal {{
            background: {border};
            min-width: 20px;
            border-radius: 4px;
        }}
        
        QScrollBar::handle:horizontal:hover {{
            background: {accent};
        }}
        """
        self.setStyleSheet(style)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Elafrý")
    window = BrowserWindow()
    window.show()
    sys.exit(app.exec())

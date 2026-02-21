DARK_THEME_STYLESHEET = """
QWidget {
    background-color: #2b2b2b;
    color: #f0f0f0;
    font-family: "Segoe UI", "Cantarell", "sans-serif";
    font-size: 10pt;
}

QMainWindow {
    background-color: #2b2b2b;
}

QTabWidget#Ribbon::pane {
    border: 1px solid #3c3c3c;
}

QTabWidget#Ribbon::tab-bar {
    alignment: left;
}

QTabBar#Ribbon::tab {
    background: #2b2b2b;
    color: #f0f0f0;
    padding: 8px 16px;
    border: 1px solid #3c3c3c;
    border-bottom: none;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}

QTabBar#Ribbon::tab:selected {
    background: #3c3c3c;
    margin-bottom: -1px; /* Pull tab up */
}

QTabBar#Ribbon::tab:hover {
    background: #4a4a4a;
}

QToolBar {
    background: #3c3c3c;
    border: none;
    padding: 4px;
    spacing: 4px;
}

QToolButton {
    background: transparent;
    border: 1px solid transparent;
    padding: 4px;
    border-radius: 4px;
}

QToolButton:hover {
    background: #4a4a4a;
    border: 1px solid #5a5a5a;
}

QToolButton:pressed {
    background: #5a5a5a;
}

QToolButton:checked {
    background: #5a5a5a;
    border: 1px solid #6a6a6a;
}

QSplitter::handle {
    background-color: #3c3c3c;
}

QSplitter::handle:horizontal {
    width: 1px;
}

QSplitter::handle:vertical {
    height: 1px;
}

/* Sidebar */
#Sidebar {
    background-color: #252525;
    border-right: 1px solid #3c3c3c;
}

#Sidebar QLabel#WorkspaceTitle {
    font-weight: bold;
    font-size: 11pt;
    padding: 8px;
    background-color: #252525;
}

QTreeView {
    background-color: #252525;
    border: none;
    color: #f0f0f0;
}

QTreeView::item {
    padding: 6px;
    border-radius: 4px;
}

QTreeView::item:hover {
    background-color: #3c3c3c;
}

QTreeView::item:selected {
    background-color: #0078d7; /* A bright accent color */
    color: white;
}

QLineEdit {
    background-color: #3c3c3c;
    border: 1px solid #5a5a5a;
    border-radius: 4px;
    padding: 6px;
    color: #f0f0f0;
}

QLineEdit:focus {
    border: 1px solid #0078d7;
}

/* Editor Area */
QTabWidget#EditorTabs::pane {
    border: none;
    background-color: #2b2b2b;
}

QTabBar#EditorTabs::tab {
    background: #2b2b2b;
    border: 1px solid #3c3c3c;
    border-bottom: none;
    padding: 8px 16px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}

QTabBar#EditorTabs::tab:selected {
    background: #383838;
}

QTabBar#EditorTabs::tab:!selected {
    background: #2b2b2b;
}

QTabBar#EditorTabs::tab:hover {
    background: #4a4a4a;
}

QTextEdit {
    background-color: #383838; /* Slightly lighter for contrast */
    border: 1px solid #4a4a4a;
    border-radius: 4px;
    color: #f0f0f0;
    padding: 40px; /* Simulate page margins */
}

/* Scrollbars */
QScrollBar:vertical {
    border: none;
    background: #2b2b2b;
    width: 12px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: #4a4a4a;
    min-height: 20px;
    border-radius: 6px;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}

QScrollBar:horizontal {
    border: none;
    background: #2b2b2b;
    height: 12px;
    margin: 0;
}

QScrollBar::handle:horizontal {
    background: #4a4a4a;
    min-width: 20px;
    border-radius: 6px;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0;
}

QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
    background: none;
}

QStatusBar {
    background-color: #252525;
    color: #f0f0f0;
}

QDockWidget {
    titlebar-close-icon: url(close.png);
    titlebar-normal-icon: url(undock.png);
}

QDockWidget::title {
    background: #3c3c3c;
    text-align: left;
    padding: 5px;
}
"""

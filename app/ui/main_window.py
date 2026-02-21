import os
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTabWidget, QSplitter, QToolBar, 
    QComboBox, QSpinBox, QColorDialog, QFileDialog, QMessageBox, QLabel, 
    QDockWidget, QStatusBar
)
from PySide6.QtGui import QAction, QIcon, QFontDatabase, QKeySequence, QTextCursor, QTextListFormat, QColor, QFont, QTextCharFormat
from PySide6.QtCore import Qt, QSize
import qtawesome as qta

from app.ui.sidebar_widget import SidebarWidget
from app.ui.editor_widget import EditorWidget
from app.services.file_manager import FileManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Draftwise")
        self.resize(1200, 800)

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Splitter
        self.splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(self.splitter)

        # Sidebar
        self.sidebar = SidebarWidget()
        self.sidebar.file_opened.connect(self.open_file)
        self.splitter.addWidget(self.sidebar)

        # Tab Widget (Editors)
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.splitter.addWidget(self.tabs)
        
        # Adjust Splitter Sizes
        self.splitter.setSizes([250, 950])

        # Setup UI
        self.create_actions()
        self.create_toolbar()
        self.create_menus()
        self.create_statusbar()

        # Apply Styles
        self.apply_styles()

        # Open a default "Untitled" tab
        self.new_file()

    def create_actions(self):
        # File Actions
        self.new_act = QAction(qta.icon('fa5s.file'), "New", self)
        self.new_act.setShortcut(QKeySequence.New)
        self.new_act.triggered.connect(self.new_file)

        self.open_act = QAction(qta.icon('fa5s.folder-open'), "Open", self)
        self.open_act.setShortcut(QKeySequence.Open)
        self.open_act.triggered.connect(self.open_file_dialog)

        self.save_act = QAction(qta.icon('fa5s.save'), "Save", self)
        self.save_act.setShortcut(QKeySequence.Save)
        self.save_act.triggered.connect(self.save_file)

        # Format Actions
        self.bold_act = QAction(qta.icon('fa5s.bold'), "Bold", self)
        self.bold_act.setCheckable(True)
        self.bold_act.setShortcut(QKeySequence.Bold)
        self.bold_act.triggered.connect(self.format_bold)

        self.italic_act = QAction(qta.icon('fa5s.italic'), "Italic", self)
        self.italic_act.setCheckable(True)
        self.italic_act.setShortcut(QKeySequence.Italic)
        self.italic_act.triggered.connect(self.format_italic)

        self.underline_act = QAction(qta.icon('fa5s.underline'), "Underline", self)
        self.underline_act.setCheckable(True)
        self.underline_act.setShortcut(QKeySequence.Underline)
        self.underline_act.triggered.connect(self.format_underline)

        self.left_align_act = QAction(qta.icon('fa5s.align-left'), "Left Align", self)
        self.left_align_act.triggered.connect(lambda: self.format_alignment(Qt.AlignLeft))

        self.center_align_act = QAction(qta.icon('fa5s.align-center'), "Center Align", self)
        self.center_align_act.triggered.connect(lambda: self.format_alignment(Qt.AlignCenter))

        self.right_align_act = QAction(qta.icon('fa5s.align-right'), "Right Align", self)
        self.right_align_act.triggered.connect(lambda: self.format_alignment(Qt.AlignRight))

        self.justify_align_act = QAction(qta.icon('fa5s.align-justify'), "Justify", self)
        self.justify_align_act.triggered.connect(lambda: self.format_alignment(Qt.AlignJustify))

        self.color_act = QAction(qta.icon('fa5s.palette'), "Text Color", self)
        self.color_act.triggered.connect(self.format_color)

        self.highlight_act = QAction(qta.icon('fa5s.highlighter'), "Highlight", self)
        self.highlight_act.triggered.connect(self.format_highlight)

    def create_toolbar(self):
        self.toolbar = QToolBar("Formatting")
        self.toolbar.setIconSize(QSize(18, 18))
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)

        self.toolbar.addAction(self.new_act)
        self.toolbar.addAction(self.open_act)
        self.toolbar.addAction(self.save_act)
        self.toolbar.addSeparator()

        # Font Selection
        self.font_combo = QComboBox()
        self.font_combo.addItems(QFontDatabase.families())
        self.font_combo.setCurrentText("Calibri")
        self.font_combo.currentTextChanged.connect(self.format_font_family)
        self.toolbar.addWidget(self.font_combo)

        # Font Size
        self.size_spin = QSpinBox()
        self.size_spin.setRange(8, 72)
        self.size_spin.setValue(12)
        self.size_spin.valueChanged.connect(self.format_font_size)
        self.toolbar.addWidget(self.size_spin)

        self.toolbar.addSeparator()
        self.toolbar.addAction(self.bold_act)
        self.toolbar.addAction(self.italic_act)
        self.toolbar.addAction(self.underline_act)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.left_align_act)
        self.toolbar.addAction(self.center_align_act)
        self.toolbar.addAction(self.right_align_act)
        self.toolbar.addAction(self.justify_align_act)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.color_act)
        self.toolbar.addAction(self.highlight_act)

    def create_menus(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        file_menu.addAction(self.new_act)
        file_menu.addAction(self.open_act)
        file_menu.addAction(self.save_act)
        
        edit_menu = menubar.addMenu("Edit")
        # Add basic edit actions later (Undo/Redo provided by QTextEdit context menu mostly)

    def create_statusbar(self):
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.status_label = QLabel("Ready")
        self.statusbar.addWidget(self.status_label)

    def apply_styles(self):
        # Basic Material-ish Dark Theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QToolBar {
                background-color: #ffffff;
                border-bottom: 1px solid #e0e0e0;
                spacing: 5px;
                padding: 5px;
            }
            QToolBar QToolButton {
                border-radius: 4px;
                padding: 4px;
            }
            QToolBar QToolButton:hover {
                background-color: #e0e0e0;
            }
            QTabWidget::pane {
                border: 1px solid #e0e0e0;
                background-color: #e0e0e0; /* Background behind pages */
            }
            QTabBar::tab {
                background: #f0f0f0;
                border: 1px solid #d0d0d0;
                padding: 8px 12px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom-color: white;
                font-weight: bold;
            }
            QSplitter::handle {
                background-color: #d0d0d0;
            }
        """)

    # --- Editor Management ---

    def current_editor(self):
        widget = self.tabs.currentWidget()
        if isinstance(widget, EditorWidget):
            return widget
        return None

    def new_file(self):
        editor = EditorWidget(parent=self)
        self.tabs.addTab(editor, "Untitled")
        self.tabs.setCurrentWidget(editor)
        editor.content_changed.connect(lambda: self.status_label.setText("Modified"))

    def open_file_dialog(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;Text Files (*.txt);;Markdown (*.md);;Word (*.docx);;PDF (*.pdf)")
        if path:
            self.open_file(path)

    def open_file(self, path):
        # Check if already open
        for i in range(self.tabs.count()):
            widget = self.tabs.widget(i)
            if isinstance(widget, EditorWidget) and widget.file_path == path:
                self.tabs.setCurrentIndex(i)
                return

        # Load file
        data = FileManager.read_file(path)
        editor = EditorWidget(file_path=path, parent=self)
        editor.set_content(data['content'], data['format'])
        
        self.tabs.addTab(editor, os.path.basename(path))
        self.tabs.setCurrentWidget(editor)
        self.status_label.setText(f"Opened {path}")

    def save_file(self):
        editor = self.current_editor()
        if not editor:
            return

        if not editor.file_path:
            path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Word (*.docx);;Text Files (*.txt);;Markdown (*.md);;PDF (*.pdf)")
            if not path:
                return
            editor.file_path = path
            self.tabs.setTabText(self.tabs.currentIndex(), os.path.basename(path))

        content_html = editor.get_content_html()
        content_plain = editor.get_content_plain()
        
        try:
            FileManager.save_file(editor.file_path, content_html, content_plain)
            self.status_label.setText(f"Saved {editor.file_path}")
            editor.is_modified = False
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not save file: {str(e)}")

    def close_tab(self, index):
        widget = self.tabs.widget(index)
        if isinstance(widget, EditorWidget) and widget.is_modified:
            reply = QMessageBox.question(self, "Unsaved Changes", "Save changes before closing?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                self.save_file()
            elif reply == QMessageBox.Cancel:
                return
        self.tabs.removeTab(index)

    # --- Formatting Handlers ---

    def format_bold(self):
        if self.current_editor(): self.current_editor().toggle_bold()

    def format_italic(self):
        if self.current_editor(): self.current_editor().toggle_italic()

    def format_underline(self):
        if self.current_editor(): self.current_editor().toggle_underline()

    def format_alignment(self, align):
        if self.current_editor(): self.current_editor().set_alignment(align)

    def format_color(self):
        if self.current_editor():
            color = QColorDialog.getColor()
            if color.isValid():
                self.current_editor().set_text_color(color)

    def format_highlight(self):
        if self.current_editor():
            color = QColorDialog.getColor()
            if color.isValid():
                self.current_editor().set_highlight_color(color)

    def format_font_family(self, font_name):
        if self.current_editor():
            fmt = QTextCharFormat()
            fmt.setFontFamilies([font_name])
            self.current_editor().merge_format_on_word_or_selection(fmt)

    def format_font_size(self, size):
        if self.current_editor():
            fmt = QTextCharFormat()
            fmt.setFontPointSize(size)
            self.current_editor().merge_format_on_word_or_selection(fmt)

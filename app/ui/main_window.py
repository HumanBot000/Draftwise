import os
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QSplitter,
    QToolBar, QComboBox, QSpinBox, QColorDialog, QFileDialog, QMessageBox,
    QLabel, QDockWidget
)
from PySide6.QtGui import QAction, QIcon, QFontDatabase, QKeySequence
from PySide6.QtCore import Qt, QSize
import qtawesome as qta

from app.ui.sidebar_widget import SidebarWidget
from app.ui.editor_widget import EditorWidget
from app.services.file_manager import FileManager
from app.ui.scholar_browser_widget import ScholarBrowserWidget

class MainWindow(QMainWindow):
    def __init__(self, workspace_path):
        super().__init__()
        self.workspace_path = workspace_path
        self.setWindowTitle(f"Draftwise - {os.path.basename(workspace_path)}")
        self.resize(1400, 900)

        # Create main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- UI Components ---
        self.create_actions()
        
        # Sidebar (Permanent)
        self.sidebar = SidebarWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.set_workspace(self.workspace_path)
        main_layout.addWidget(self.sidebar, 1) # Stretch factor 1

        # Main Content Area
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        main_layout.addWidget(content_widget, 4) # Stretch factor 4

        # Ribbon Toolbar
        self.ribbon = self.create_ribbon()
        content_layout.addWidget(self.ribbon)

        # Editor Area
        self.tabs = QTabWidget()
        self.tabs.setObjectName("EditorTabs")
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        content_layout.addWidget(self.tabs)
        
        self.create_docks()
        self.create_statusbar()

        # --- Connections ---
        self.sidebar.file_opened.connect(self.open_file)

        # Open a default "Untitled" tab
        self.new_file()

    def create_actions(self):
        # File
        self.new_act = QAction(qta.icon('fa5s.file', color='white'), "New", self)
        self.open_act = QAction(qta.icon('fa5s.folder-open', color='white'), "Open", self)
        self.save_act = QAction(qta.icon('fa5s.save', color='white'), "Save", self)
        # Format
        self.bold_act = QAction(qta.icon('fa5s.bold', color='white'), "Bold", self, checkable=True)
        self.italic_act = QAction(qta.icon('fa5s.italic', color='white'), "Italic", self, checkable=True)
        self.underline_act = QAction(qta.icon('fa5s.underline', color='white'), "Underline", self, checkable=True)
        # Alignment
        self.left_align_act = QAction(qta.icon('fa5s.align-left', color='white'), "Left", self)
        self.center_align_act = QAction(qta.icon('fa5s.align-center', color='white'), "Center", self)
        self.right_align_act = QAction(qta.icon('fa5s.align-right', color='white'), "Right", self)
        self.justify_align_act = QAction(qta.icon('fa5s.align-justify', color='white'), "Justify", self)
        # Color
        self.color_act = QAction(qta.icon('fa5s.palette', color='white'), "Color", self)
        # Scholar
        self.scholar_search_act = QAction(qta.icon('fa5s.book-open', color='white'), "Scholar", self)

        # --- Connections for Actions ---
        self.new_act.triggered.connect(self.new_file)
        self.open_act.triggered.connect(self.open_file_dialog)
        self.save_act.triggered.connect(self.save_file)
        self.bold_act.triggered.connect(self.format_bold)
        self.italic_act.triggered.connect(self.format_italic)
        self.underline_act.triggered.connect(self.format_underline)
        self.left_align_act.triggered.connect(lambda: self.format_alignment(Qt.AlignLeft))
        self.center_align_act.triggered.connect(lambda: self.format_alignment(Qt.AlignCenter))
        self.right_align_act.triggered.connect(lambda: self.format_alignment(Qt.AlignRight))
        self.justify_align_act.triggered.connect(lambda: self.format_alignment(Qt.AlignJustify))
        self.color_act.triggered.connect(self.format_color)
        self.scholar_search_act.triggered.connect(self.toggle_scholar_dock)

    def create_ribbon(self):
        ribbon_bar = QToolBar("Main Toolbar")
        ribbon_bar.setIconSize(QSize(20, 20))
        ribbon_bar.setMovable(False)

        ribbon_bar.addAction(self.new_act)
        ribbon_bar.addAction(self.open_act)
        ribbon_bar.addAction(self.save_act)
        ribbon_bar.addSeparator()

        self.font_combo = QComboBox()
        self.font_combo.addItems(QFontDatabase.families())
        self.font_combo.setCurrentText("Calibri")
        self.font_combo.currentTextChanged.connect(self.format_font_family)
        ribbon_bar.addWidget(self.font_combo)

        self.size_spin = QSpinBox()
        self.size_spin.setRange(8, 72)
        self.size_spin.setValue(12)
        self.size_spin.valueChanged.connect(self.format_font_size)
        ribbon_bar.addWidget(self.size_spin)
        ribbon_bar.addSeparator()

        ribbon_bar.addAction(self.bold_act)
        ribbon_bar.addAction(self.italic_act)
        ribbon_bar.addAction(self.underline_act)
        ribbon_bar.addSeparator()

        ribbon_bar.addAction(self.left_align_act)
        ribbon_bar.addAction(self.center_align_act)
        ribbon_bar.addAction(self.right_align_act)
        ribbon_bar.addAction(self.justify_align_act)
        ribbon_bar.addSeparator()
        
        ribbon_bar.addAction(self.color_act)
        ribbon_bar.addSeparator()
        
        ribbon_bar.addAction(self.scholar_search_act)
        
        return ribbon_bar

    def create_statusbar(self):
        self.status_bar = self.statusBar()
        self.status_label = QLabel("Ready")
        self.status_bar.addPermanentWidget(self.status_label)

    def create_docks(self):
        self.scholar_dock = QDockWidget("Scholar Browser", self)
        self.scholar_browser = ScholarBrowserWidget(self.workspace_path)
        self.scholar_dock.setWidget(self.scholar_browser)
        self.addDockWidget(Qt.RightDockWidgetArea, self.scholar_dock)
        self.scholar_dock.hide()
        self.scholar_browser.paper_imported.connect(self.sidebar.refresh)

    def toggle_scholar_dock(self):
        self.scholar_dock.setVisible(not self.scholar_dock.isVisible())

    def current_editor(self):
        return self.tabs.currentWidget()

    def new_file(self):
        editor = EditorWidget(parent=self)
        self.tabs.addTab(editor, "Untitled")
        self.tabs.setCurrentWidget(editor)
        editor.content_changed.connect(lambda: self.status_label.setText("Modified"))

    def open_file_dialog(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open File", self.workspace_path, "All Files (*)")
        if path:
            self.open_file(path)

    def open_file(self, path):
        for i in range(self.tabs.count()):
            if self.tabs.widget(i).file_path == path:
                self.tabs.setCurrentIndex(i)
                return
        
        data = FileManager.read_file(path)
        editor = EditorWidget(file_path=path, parent=self)
        editor.set_content(data['content'], data['format'])
        
        self.tabs.addTab(editor, os.path.basename(path))
        self.tabs.setCurrentWidget(editor)
        self.status_label.setText(f"Opened {os.path.basename(path)}")

    def save_file(self):
        editor = self.current_editor()
        if not editor: return

        path = editor.file_path
        if not path:
            path, _ = QFileDialog.getSaveFileName(self, "Save File", self.workspace_path, "Word (*.docx);;Text (*.txt)")
            if not path: return
            editor.file_path = path
            self.tabs.setTabText(self.tabs.currentIndex(), os.path.basename(path))

        try:
            FileManager.save_file(path, editor.get_content_html(), editor.get_content_plain())
            self.status_label.setText(f"Saved {os.path.basename(path)}")
            editor.is_modified = False
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not save file: {e}")

    def close_tab(self, index):
        editor = self.tabs.widget(index)
        if editor.is_modified:
            reply = QMessageBox.question(self, "Unsaved Changes", "Save changes before closing?",
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Yes: self.save_file()
            elif reply == QMessageBox.Cancel: return
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
            if color.isValid(): self.current_editor().set_text_color(color)
    def format_font_family(self, font_name):
        if self.current_editor(): self.current_editor().set_font_family(font_name)
    def format_font_size(self, size):
        if self.current_editor(): self.current_editor().set_font_size(size)

from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QFrame
from PySide6.QtGui import QTextDocument, QFont, QTextCursor, QAction, QColor, QTextCharFormat, QTextBlockFormat, QPageSize
from PySide6.QtCore import Qt, Signal, QTimer

class EditorWidget(QWidget):
    content_changed = Signal()

    def __init__(self, file_path=None, parent=None):
        super().__init__(parent)
        self.file_path = file_path
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Editor Area (The "Page")
        self.editor = QTextEdit()
        self.editor.setFrameShape(QFrame.NoFrame)
        self.editor.setAcceptRichText(True)
        
        # Simulate A4 Page feel
        # A4 width is approx 210mm. At 96 DPI -> ~794px.
        # We add some padding for comfort.
        self.editor.setStyleSheet("""
            QTextEdit {
                background-color: white; 
                color: black;
                padding: 40px;
                font-family: 'Calibri', 'Arial', sans-serif;
                font-size: 14px;
                selection-background-color: #B3D7FF;
            }
        """)

        # Set default font
        font = QFont("Calibri", 12)
        self.editor.setFont(font)
        
        self.layout.addWidget(self.editor)

        # Connect signals
        self.editor.textChanged.connect(self.on_text_changed)

        # Auto-save setup
        self.autosave_timer = QTimer(self)
        self.autosave_timer.setInterval(5000) # Autosave every 5 seconds
        self.autosave_timer.timeout.connect(self.autosave)
        self.autosave_timer.start()
        
        self.is_modified = False

    def on_text_changed(self):
        self.is_modified = True
        self.content_changed.emit()

    def set_content(self, content, format='plain'):
        if format == 'html':
            self.editor.setHtml(content)
        else:
            self.editor.setPlainText(content)
        self.is_modified = False

    def get_content_html(self):
        return self.editor.toHtml()

    def get_content_plain(self):
        return self.editor.toPlainText()

    def autosave(self):
        if self.is_modified and self.file_path:
            # Emit a signal or call a service to save
            # For simplicity in this demo, we print.
            # In a real app, we'd call a controller method.
            print(f"Auto-saving {self.file_path}...")
            # We don't implement actual file writing here to keep UI decoupled from IO logic.
            # The controller should handle the actual save call.
            pass

    # Formatting Methods
    def toggle_bold(self):
        fmt = QTextCharFormat()
        fmt.setFontWeight(QFont.Bold if self.editor.fontWeight() != QFont.Bold else QFont.Normal)
        self.merge_format_on_word_or_selection(fmt)

    def toggle_italic(self):
        fmt = QTextCharFormat()
        fmt.setFontItalic(not self.editor.fontItalic())
        self.merge_format_on_word_or_selection(fmt)

    def toggle_underline(self):
        fmt = QTextCharFormat()
        fmt.setFontUnderline(not self.editor.fontUnderline())
        self.merge_format_on_word_or_selection(fmt)
        
    def set_alignment(self, alignment):
        self.editor.setAlignment(alignment)

    def set_text_color(self, color):
        fmt = QTextCharFormat()
        fmt.setForeground(color)
        self.merge_format_on_word_or_selection(fmt)
        
    def set_highlight_color(self, color):
        fmt = QTextCharFormat()
        fmt.setBackground(color)
        self.merge_format_on_word_or_selection(fmt)

    def merge_format_on_word_or_selection(self, format):
        cursor = self.editor.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.WordUnderCursor)
        cursor.mergeCharFormat(format)
        self.editor.mergeCurrentCharFormat(format)

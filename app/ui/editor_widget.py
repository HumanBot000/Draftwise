from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QFrame
from PySide6.QtGui import QFont, QTextCursor, QColor, QTextCharFormat
from PySide6.QtCore import Qt, Signal

class EditorWidget(QWidget):
    content_changed = Signal()

    def __init__(self, file_path=None, parent=None):
        super().__init__(parent)
        self.file_path = file_path
        self.is_modified = False

        self.layout = QVBoxLayout(self)
        # Center the editor with margins, creating a "page" effect
        self.layout.setContentsMargins(50, 20, 50, 20)
        self.layout.setSpacing(0)

        # Editor
        self.editor = QTextEdit()
        self.editor.setFrameShape(QFrame.NoFrame)
        self.editor.setObjectName("Editor") # For specific styling
        
        # Set default font
        font = QFont("Calibri", 12)
        self.editor.setFont(font)
        
        self.layout.addWidget(self.editor)

        # --- Connections ---
        self.editor.textChanged.connect(self.on_text_changed)

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

    # --- Formatting Methods ---
    def toggle_bold(self):
        self.editor.setFontWeight(QFont.Bold if self.editor.fontWeight() != QFont.Bold else QFont.Normal)

    def toggle_italic(self):
        self.editor.setFontItalic(not self.editor.fontItalic())

    def toggle_underline(self):
        self.editor.setFontUnderline(not self.editor.fontUnderline())
        
    def set_alignment(self, alignment):
        self.editor.setAlignment(alignment)

    def set_text_color(self, color):
        self.editor.setTextColor(color)
        
    def set_font_family(self, font_family):
        fmt = QTextCharFormat()
        fmt.setFontFamilies([font_family])
        self.merge_format_on_word_or_selection(fmt)

    def set_font_size(self, size):
        fmt = QTextCharFormat()
        fmt.setFontPointSize(size)
        self.merge_format_on_word_or_selection(fmt)

    def merge_format_on_word_or_selection(self, format_to_merge):
        cursor = self.editor.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.WordUnderCursor)
        
        # We need to merge, not replace the format
        current_format = cursor.charFormat()
        current_format.merge(format_to_merge)
        cursor.setCharFormat(current_format)
        
        # This ensures the new format is applied to subsequent typing
        self.editor.setCurrentCharFormat(current_format)

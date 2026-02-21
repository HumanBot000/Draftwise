import sys
import os
from PySide6.QtWidgets import QApplication, QFileDialog, QWidget

# Add project root to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app.ui.main_window import MainWindow
from app.ui.styles import DARK_THEME_STYLESHEET

def main():
    app = QApplication(sys.argv)
    
    # It's better to apply the stylesheet before creating any widgets
    app.setStyleSheet(DARK_THEME_STYLESHEET)
    
    workspace_path = select_workspace()
    if not workspace_path:
        sys.exit(0)

    window = MainWindow(workspace_path=workspace_path)
    window.show()
    
    sys.exit(app.exec())

def select_workspace():
    """Opens a dialog for workspace selection."""
    # Using a temporary widget for the dialog parent
    temp_widget = QWidget()
    path = QFileDialog.getExistingDirectory(
        temp_widget,
        "Select Workspace Directory",
        os.path.expanduser("~")
    )
    temp_widget.deleteLater()
    return path

if __name__ == "__main__":
    main()

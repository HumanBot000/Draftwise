import sys
import os
from PySide6.QtWidgets import QApplication

# Add project root to sys.path to allow absolute imports like 'from app.ui...'
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app.ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion") 
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

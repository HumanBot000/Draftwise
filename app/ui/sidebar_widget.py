from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTreeView, QFileSystemModel, QMenu, QLineEdit,
    QInputDialog, QMessageBox, QLabel, QPushButton, QHBoxLayout
)
from PySide6.QtCore import QDir, Qt, Signal, QModelIndex
from PySide6.QtGui import QAction
import os
import shutil
import qtawesome as qta

class SidebarWidget(QWidget):
    file_opened = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.workspace_path = None
        self.setObjectName("Sidebar")

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Workspace Header
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(10, 10, 10, 10)
        self.title_label = QLabel("WORKSPACE")
        self.title_label.setObjectName("WorkspaceTitle")
        self.refresh_btn = QPushButton(qta.icon('fa5s.sync-alt', color='white'), "")
        self.refresh_btn.setToolTip("Refresh Workspace")
        self.refresh_btn.setFlat(True)
        header_layout.addWidget(self.title_label, 1)
        header_layout.addWidget(self.refresh_btn)
        self.layout.addWidget(header_widget)

        # File System Model
        self.model = QFileSystemModel()
        self.model.setReadOnly(False)
        self.model.setFilter(QDir.AllEntries | QDir.NoDotAndDotDot)
        
        # Tree View
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setAnimated(True)
        self.tree.setIndentation(15)
        self.tree.setSortingEnabled(True)
        self.tree.sortByColumn(0, Qt.AscendingOrder)
        self.tree.setDragDropMode(QTreeView.InternalMove)
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        
        # Hide unnecessary columns
        for i in range(1, self.model.columnCount()):
            self.tree.hideColumn(i)
        self.tree.setHeaderHidden(True)
        
        self.layout.addWidget(self.tree)

        # --- Connections ---
        self.tree.doubleClicked.connect(self.on_double_click)
        self.tree.customContextMenuRequested.connect(self.open_context_menu)
        self.refresh_btn.clicked.connect(self.refresh)

    def set_workspace(self, path):
        self.workspace_path = path
        self.model.setRootPath(path)
        self.tree.setRootIndex(self.model.index(path))
        self.title_label.setText(os.path.basename(path).upper())

    def on_double_click(self, index):
        if not self.model.isDir(index):
            self.file_opened.emit(self.model.filePath(index))

    def open_context_menu(self, position):
        index = self.tree.indexAt(position)
        menu = QMenu()

        new_file_act = QAction(qta.icon('fa5s.file', color='white'), "New File", self)
        new_folder_act = QAction(qta.icon('fa5s.folder', color='white'), "New Folder", self)
        
        base_path = self.model.filePath(index) if index.isValid() else self.workspace_path
        if not os.path.isdir(base_path):
            base_path = os.path.dirname(base_path)

        new_file_act.triggered.connect(lambda: self.create_new_file(base_path))
        new_folder_act.triggered.connect(lambda: self.create_new_folder(base_path))

        menu.addAction(new_file_act)
        menu.addAction(new_folder_act)

        if index.isValid():
            menu.addSeparator()
            rename_act = QAction(qta.icon('fa5s.pencil-alt', color='white'), "Rename", self)
            delete_act = QAction(qta.icon('fa5s.trash-alt', color='white'), "Delete", self)
            
            rename_act.triggered.connect(lambda: self.rename_item(index))
            delete_act.triggered.connect(lambda: self.delete_item(index))
            
            menu.addAction(rename_act)
            menu.addAction(delete_act)
            
        menu.exec(self.tree.viewport().mapToGlobal(position))

    def create_new_file(self, base_path):
        name, ok = QInputDialog.getText(self, "New File", "Enter file name (e.g., report.docx):")
        if ok and name:
            try:
                open(os.path.join(base_path, name), 'a').close()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not create file: {e}")

    def create_new_folder(self, base_path):
        name, ok = QInputDialog.getText(self, "New Folder", "Enter folder name:")
        if ok and name:
            try:
                os.makedirs(os.path.join(base_path, name), exist_ok=True)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not create folder: {e}")

    def rename_item(self, index):
        old_path = self.model.filePath(index)
        old_name = self.model.fileName(index)
        new_name, ok = QInputDialog.getText(self, "Rename", "Enter new name:", text=old_name)
        if ok and new_name and new_name != old_name:
            new_path = os.path.join(os.path.dirname(old_path), new_name)
            if self.model.isDir(index):
                QMessageBox.warning(self, "Unsupported", "Renaming folders is not yet supported from the UI.")
                return # QFileSystemModel doesn't directly support renaming dirs well
            if not self.model.rename(index, new_name):
                 QMessageBox.critical(self, "Error", "Could not rename the item.")

    def delete_item(self, index):
        path = self.model.filePath(index)
        is_dir = self.model.isDir(index)
        
        reply = QMessageBox.question(self, "Delete", f"Are you sure you want to delete {os.path.basename(path)}?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            if is_dir:
                success = self.model.rmdir(index)
            else:
                success = self.model.remove(index)
            
            if not success:
                # Fallback for non-empty directories
                if is_dir and not os.listdir(path): # Check if it failed because it was empty
                    try:
                        shutil.rmtree(path)
                        self.refresh()
                    except Exception as e:
                        QMessageBox.critical(self, "Error", f"Could not delete directory: {e}")
                else:
                    QMessageBox.critical(self, "Error", "Could not delete the item. It might not be empty.")

    def refresh(self):
        """Forces the model to refresh its data from the file system."""
        self.model.setRootPath("") # Invalidate current view
        self.model.setRootPath(self.workspace_path)
        self.tree.setRootIndex(self.model.index(self.workspace_path))

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTreeView, QFileSystemModel, QMenu, QLineEdit, 
    QInputDialog, QMessageBox, QHeaderView, QLabel, QPushButton, QHBoxLayout
)
from PySide6.QtCore import QDir, Qt, Signal, QModelIndex
import os
import shutil
import qtawesome as qta

class SidebarWidget(QWidget):
    file_opened = Signal(str)
    workspace_changed = Signal(str)

    def __init__(self, workspace_path=None, parent=None):
        super().__init__(parent)
        self.workspace_path = workspace_path
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)

        # Workspace Header
        header_layout = QHBoxLayout()
        self.title_label = QLabel("WORKSPACE")
        self.title_label.setStyleSheet("font-weight: bold; color: #bb86fc; letter-spacing: 1px;")
        header_layout.addWidget(self.title_label)
        
        self.change_ws_btn = QPushButton(qta.icon('fa5s.cog', color='#888888'), "")
        self.change_ws_btn.setToolTip("Change Workspace")
        self.change_ws_btn.setFixedSize(24, 24)
        self.change_ws_btn.setStyleSheet("border: none; background: transparent;")
        header_layout.addWidget(self.change_ws_btn)
        self.layout.addLayout(header_layout)

        # Search Bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search documents...")
        self.search_bar.setStyleSheet("""
            QLineEdit {
                background-color: #2d2d2d;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                padding: 5px;
                color: #e0e0e0;
            }
        """)
        self.layout.addWidget(self.search_bar)

        # File System Model
        self.model = QFileSystemModel()
        self.model.setReadOnly(False)
        self.model.setNameFilterDisables(False)

        # Tree View
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setAnimated(True)
        self.tree.setIndentation(20)
        self.tree.setSortingEnabled(True)
        self.tree.setDragEnabled(True)
        self.tree.setAcceptDrops(True)
        self.tree.setDropIndicatorShown(True)
        self.tree.setEditTriggers(QTreeView.EditKeyPressed | QTreeView.SelectedClicked)
        
        self.tree.hideColumn(1)
        self.tree.hideColumn(2)
        self.tree.hideColumn(3)
        self.tree.header().hide()
        
        self.tree.setStyleSheet("""
            QTreeView {
                background-color: transparent;
                border: none;
                color: #b0b0b0;
            }
            QTreeView::item:hover {
                background-color: #3d3d3d;
            }
            QTreeView::item:selected {
                background-color: #4d4d4d;
                color: #ffffff;
            }
        """)
        
        self.layout.addWidget(self.tree)

        if self.workspace_path:
            self.set_workspace(self.workspace_path)

        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.open_context_menu)
        self.tree.doubleClicked.connect(self.on_double_click)
        self.search_bar.textChanged.connect(self.filter_files)

    def set_workspace(self, path):
        self.workspace_path = path
        self.model.setRootPath(path)
        self.tree.setRootIndex(self.model.index(path))
        self.model.setNameFilters(["*.txt", "*.md", "*.docx", "*.pdf"])
        self.workspace_changed.emit(path)

    def filter_files(self, text):
        if text:
            self.model.setNameFilters([f"*{text}*"])
        else:
            self.model.setNameFilters(["*.txt", "*.md", "*.docx", "*.pdf"])

    def on_double_click(self, index):
        file_path = self.model.filePath(index)
        if os.path.isfile(file_path):
            self.file_opened.emit(file_path)

    def open_context_menu(self, position):
        index = self.tree.indexAt(position)
        menu = QMenu()

        new_file_action = menu.addAction("New File")
        new_folder_action = menu.addAction("New Folder")
        menu.addSeparator()
        
        if index.isValid():
            rename_action = menu.addAction("Rename")
            delete_action = menu.addAction("Delete")
            
            action = menu.exec(self.tree.viewport().mapToGlobal(position))
            
            if action == rename_action:
                self.rename_item(index)
            elif action == delete_action:
                self.delete_item(index)
            elif action == new_file_action:
                self.create_new_file(index)
            elif action == new_folder_action:
                self.create_new_folder(index)
        else:
            # Context menu on empty space
            new_file_action = menu.addAction("New File")
            new_folder_action = menu.addAction("New Folder")
            
            action = menu.exec(self.tree.viewport().mapToGlobal(position))
            
            if action == new_file_action:
                self.create_new_file(self.tree.rootIndex())
            elif action == new_folder_action:
                self.create_new_folder(self.tree.rootIndex())

    def create_new_file(self, parent_index):
        base_path = self.model.filePath(parent_index)
        if os.path.isfile(base_path):
            base_path = os.path.dirname(base_path)
            
        name, ok = QInputDialog.getText(self, "New File", "Enter file name:")
        if ok and name:
            full_path = os.path.join(base_path, name)
            try:
                with open(full_path, 'w') as f:
                    pass
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def create_new_folder(self, parent_index):
        base_path = self.model.filePath(parent_index)
        if os.path.isfile(base_path):
            base_path = os.path.dirname(base_path)

        name, ok = QInputDialog.getText(self, "New Folder", "Enter folder name:")
        if ok and name:
            full_path = os.path.join(base_path, name)
            try:
                os.makedirs(full_path)
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def rename_item(self, index):
        old_name = self.model.fileName(index)
        new_name, ok = QInputDialog.getText(self, "Rename", "Enter new name:", text=old_name)
        if ok and new_name:
            old_path = self.model.filePath(index)
            new_path = os.path.join(os.path.dirname(old_path), new_name)
            try:
                os.rename(old_path, new_path)
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def delete_item(self, index):
        path = self.model.filePath(index)
        reply = QMessageBox.question(self, "Delete", f"Are you sure you want to delete {path}?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

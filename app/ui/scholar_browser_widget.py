import sys
import os
import re
import requests
from PySide6.QtWidgets import (
    QWidget, QApplication, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QListWidget, QListWidgetItem, QLabel, QMessageBox
)
from PySide6.QtCore import Qt, Signal, QThread
import qtawesome as qta

from app.services.scholar_worker import ScholarWorker

def sanitize_filename(filename):
    """Removes invalid characters from a string to make it a valid filename."""
    return re.sub(r'[/*?:"<>|]', "", filename)

class ScholarBrowserWidget(QWidget):
    paper_imported = Signal(str)

    def __init__(self, workspace_path, parent=None):
        super().__init__(parent)
        self.workspace_path = workspace_path
        self.search_thread = None
        self.search_worker = None

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)

        # Title
        title_label = QLabel("Scholar Browser")
        title_label.setObjectName("title")
        self.layout.addWidget(title_label)

        # Search Bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search papers...")
        self.search_button = QPushButton(qta.icon('fa5s.search', color='white'), "")
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        self.layout.addLayout(search_layout)

        # Results List
        self.results_list = QListWidget()
        self.layout.addWidget(self.results_list)

        # Import Button
        self.import_button = QPushButton("Import Selected PDF")
        self.import_button.setEnabled(False)
        self.layout.addWidget(self.import_button)

        # Status Label
        self.status_label = QLabel("Ready to search.")
        self.layout.addWidget(self.status_label)

        # Connections
        self.search_button.clicked.connect(self.perform_search)
        self.search_input.returnPressed.connect(self.perform_search)
        self.results_list.itemSelectionChanged.connect(self.update_button_state)
        self.import_button.clicked.connect(self.import_paper)

    def perform_search(self):
        query = self.search_input.text()
        if not query:
            return

        self.status_label.setText("Searching...")
        self.search_button.setEnabled(False)
        self.results_list.clear()
        self.import_button.setEnabled(False)

        # Setup worker and thread
        self.search_thread = QThread()
        self.search_worker = ScholarWorker(query)
        self.search_worker.moveToThread(self.search_thread)

        # Connect signals
        self.search_worker.results_ready.connect(self.on_search_finished)
        self.search_worker.search_failed.connect(self.on_search_failed)
        self.search_thread.started.connect(self.search_worker.run)
        self.search_thread.finished.connect(self.search_thread.deleteLater)

        # Start the thread
        self.search_thread.start()

    def on_search_finished(self, results):
        self.search_button.setEnabled(True)
        if not results:
            self.status_label.setText("No results found.")
            return

        for pub in results:
            title = pub.get('bib', {}).get('title', 'No Title')
            authors = pub.get('bib', {}).get('author', 'No Authors')
            year = pub.get('bib', {}).get('pub_year', 'N/A')

            item_text = f"{title} - {authors} ({year})"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, pub)
            self.results_list.addItem(item)

        self.status_label.setText(f"Found {len(results)} results.")
        self.cleanup_search_thread()

    def on_search_failed(self, error_message):
        self.search_button.setEnabled(True)
        self.status_label.setText("Search failed.")
        QMessageBox.critical(self, "Error", f"An error occurred during search: {error_message}")
        self.cleanup_search_thread()
        
    def cleanup_search_thread(self):
        if self.search_thread and self.search_thread.isRunning():
            self.search_thread.quit()
            self.search_thread.wait()
        self.search_thread = None
        self.search_worker = None

    def update_button_state(self):
        selected = self.results_list.selectedItems()
        if not selected:
            self.import_button.setEnabled(False)
            return

        pub = selected[0].data(Qt.UserRole)
        # Check for 'eprint_url' which is often the direct PDF link
        self.import_button.setEnabled(bool(pub.get('eprint_url')))

    def import_paper(self):
        selected_items = self.results_list.selectedItems()
        if not selected_items: return

        pub = selected_items[0].data(Qt.UserRole)
        title = pub.get('bib', {}).get('title', 'untitled_paper')
        pdf_url = pub.get('eprint_url') # Prioritize eprint_url

        if not pdf_url:
            QMessageBox.warning(self, "No PDF Link", "No direct PDF link found for this paper.")
            return

        self.status_label.setText(f"Downloading '{title[:30]}...'")
        QApplication.processEvents()

        try:
            # Use a session for better connection management
            with requests.Session() as session:
                response = session.get(pdf_url, stream=True, timeout=20, headers={'User-Agent': 'Mozilla/5.0'})
                response.raise_for_status()

                # A more robust check for PDF content
                content_type = response.headers.get('Content-Type', '')
                if 'application/pdf' not in content_type and not pdf_url.endswith('.pdf'):
                     raise Exception("Linked content is not a PDF.")

                filename = sanitize_filename(title) + ".pdf"
                save_path = os.path.join(self.workspace_path, filename)

                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

                self.status_label.setText(f"Imported '{filename}'.")
                self.paper_imported.emit(save_path)

        except requests.RequestException as e:
            self.status_label.setText("Download failed.")
            QMessageBox.critical(self, "Download Error", f"Failed to download: {e}")
        except Exception as e:
            self.status_label.setText("Import failed.")
            QMessageBox.critical(self, "Import Error", f"An error occurred: {e}")
            
    def closeEvent(self, event):
        """Ensure the search thread is cleaned up when the widget is closed."""
        self.cleanup_search_thread()
        super().closeEvent(event)

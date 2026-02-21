# Draftwise - Modern Text Editor

A cross-platform desktop text editor built with Python and PySide6, designed with Material Design principles.

## Features

- **Workspace Management**: Organize files and folders in a sidebar.
- **Rich Text Editing**: WYSIWYG editor with bold, italic, underline, fonts, colors, and alignment.
- **Format Support**:
  - Import: PDF, DOCX, Markdown, TXT.
  - Export/Save: DOCX, TXT.
- **Modern UI**: Clean interface with Material Design cues.
- **Tabbed Interface**: Edit multiple documents simultaneously.
- **Auto-save**: Automatically saves changes every 5 seconds.

## Tech Stack

- **Python 3.11+**
- **PySide6** (Qt for Python)
- **python-docx** (DOCX handling)
- **PyMuPDF** (PDF reading)
- **Markdown** (MD to HTML conversion)
- **QtAwesome** (Icons)

## Setup & Installation

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Application:**
    ```bash
    python app/main.py
    ```

## Architecture

The project follows a modular structure separating UI and logic:

- **`app/main.py`**: Application entry point. Handles initialization and global styling.
- **`app/ui/`**: Contains all UI components.
  - `main_window.py`: The main application window, orchestrating the sidebar, editor tabs, and toolbar.
  - `sidebar_widget.py`: Manages the file system view and workspace operations.
  - `editor_widget.py`: The rich text editor component with "page layout" styling.
- **`app/services/`**: Contains business logic and services.
  - `file_manager.py`: Handles reading and writing of different file formats (PDF, DOCX, MD, TXT).
- **`app/models/`**: Reserved for data models (currently using standard Qt models).

from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem, QLineEdit, QFormLayout, QDialog, QDialogButtonBox, QMessageBox, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon
import folium
import os
import tempfile
from PyQt5.QtWebEngineWidgets import QWebEngineView

class NoteDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Note")

        # Create map
        self.map_view = QWebEngineView()
        self.map_file = self.create_map_html()

        # Create input fields
        self.note_edit = QLineEdit()
        self.lat_edit = QLineEdit()
        self.lon_edit = QLineEdit()

        # Layouts
        form_layout = QFormLayout()
        form_layout.addRow("Note:", self.note_edit)
        form_layout.addRow("Latitude:", self.lat_edit)
        form_layout.addRow("Longitude:", self.lon_edit)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addWidget(self.map_view)
        layout.addLayout(form_layout)
        layout.addWidget(button_box)

        self.setLayout(layout)

        # Load the map
        self.map_view.setUrl(QUrl.fromLocalFile(self.map_file))

        # Set default values for latitude and longitude
        self.lat_edit.setText("51.5074")  # Default latitude (e.g., London)
        self.lon_edit.setText("-0.1278")  # Default longitude (e.g., London)
        
    def create_map_html(self):
        # Create a temporary file for the map
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.html')
        temp_file.close()

        # Create a folium map
        map_center = [51.5074, -0.1278]  # Default center (e.g., London)
        folium_map = folium.Map(location=map_center, zoom_start=13)

        # Add a marker to the map
        folium.Marker(location=map_center, popup="You are here").add_to(folium_map)

        # Save the map to the temp HTML file
        folium_map.save(temp_file.name)

        return temp_file.name

    def get_data(self):
        return {
            'note': self.note_edit.text(),
            'latitude': self.lat_edit.text(),
            'longitude': self.lon_edit.text()
        }

class NoteItemWidget(QWidget):
    def __init__(self, note_text, delete_callback, parent=None):
        super().__init__(parent)
        self.delete_callback = delete_callback

        layout = QHBoxLayout()
        self.note_label = QLabel(note_text)
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.handle_delete)

        layout.addWidget(self.note_label)
        layout.addWidget(self.delete_button)
        self.setLayout(layout)

    def handle_delete(self):
        if QMessageBox.question(self, 'Confirm Delete', 'Are you sure you want to delete this note?',
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.Yes:
            self.delete_callback()

class MainWindow(QMainWindow):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle("MapNotes")

        self.notes_list = QListWidget()
        self.add_button = QPushButton("+ Add Note")
        
        self.add_button.clicked.connect(self.show_add_note_dialog)
        
        layout = QVBoxLayout()
        layout.addWidget(self.notes_list)
        layout.addWidget(self.add_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        self.load_notes()

    def load_notes(self):
        self.notes_list.clear()
        for index, note in enumerate(self.controller.get_notes()):
            item_widget = NoteItemWidget(
                note_text=f"{note['note']} (Lat: {note['latitude']}, Lon: {note['longitude']})",
                delete_callback=lambda i=index: self.delete_note_at(i)
            )
            item = QListWidgetItem()
            item.setSizeHint(item_widget.sizeHint())
            self.notes_list.addItem(item)
            self.notes_list.setItemWidget(item, item_widget)
    
    def show_add_note_dialog(self):
        dialog = NoteDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            self.controller.add_note(data)
            self.load_notes()
    
    def delete_note_at(self, index):
        self.controller.delete_note(index)
        self.load_notes()
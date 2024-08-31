from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QListWidget, QLineEdit, QFormLayout, QDialog, QDialogButtonBox
from PyQt5.QtCore import Qt

class NoteDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Note")
        
        self.note_edit = QLineEdit()
        self.lat_edit = QLineEdit()
        self.lon_edit = QLineEdit()
        
        layout = QFormLayout()
        layout.addRow("Note:", self.note_edit)
        layout.addRow("Latitude:", self.lat_edit)
        layout.addRow("Longitude:", self.lon_edit)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        layout.addRow(buttons)
        self.setLayout(layout)
    
    def get_data(self):
        return {
            'note': self.note_edit.text(),
            'latitude': self.lat_edit.text(),
            'longitude': self.lon_edit.text()
        }
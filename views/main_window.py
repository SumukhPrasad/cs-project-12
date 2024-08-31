from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QListWidget, QLineEdit, QFormLayout, QDialog, QDialogButtonBox
from PyQt5.QtCore import Qt

from views.note_dialog import NoteDialog

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
        for note in self.controller.get_notes():
            self.notes_list.addItem(f"{note['note']} (Lat: {note['latitude']}, Lon: {note['longitude']})")

    def show_add_note_dialog(self):
        dialog = NoteDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            self.controller.add_note(data)
            self.load_notes()
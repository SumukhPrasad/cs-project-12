from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QMessageBox

class NoteItemWidget(QWidget):
    def __init__(self, note_id, note_text, delete_callback, parent=None):
        super().__init__(parent)
        self.note_id = note_id
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
            self.delete_callback(self.note_id)
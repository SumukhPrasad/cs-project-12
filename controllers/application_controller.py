import json
import os

class ApplicationController:
    def __init__(self):
        self.notes = []
        self.load_notes()

    def get_notes(self):
        return self.notes

    def add_note(self, note_data):
        self.notes.append(note_data)
        self.save_notes()

    def save_notes(self):
        with open("notes.json", "w") as f:
            json.dump(self.notes, f)

    def delete_note(self, index):
        if 0 <= index < len(self.notes):
            del self.notes[index]
            self.save_notes()

    def load_notes(self):
        if os.path.exists("notes.json"):
            with open("notes.json", "r") as f:
                self.notes = json.load(f)

    def run(self):
        from views.main_window import MainWindow
        from PyQt5.QtWidgets import QApplication
        import sys

        app = QApplication(sys.argv)
        main_window = MainWindow(self)
        main_window.show()
        sys.exit(app.exec_())
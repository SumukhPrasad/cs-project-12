import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView  # Ensure this import is after QApplication
from controllers.application_controller import ApplicationController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Ensure to initialize QWebEngineView before any QApplication instances or components that use it
    QWebEngineView()
    controller = ApplicationController()
    controller.run()
    sys.exit(app.exec_())

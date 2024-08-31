import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView 
from controllers.application_controller import ApplicationController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # QWebEngineView must be initialised before any QApplication instances, NOT redundant
    QWebEngineView()
    controller = ApplicationController()
    controller.run()
    sys.exit(app.exec_())

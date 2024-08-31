import sys
from PyQt5.QtWidgets import QApplication
from controllers.application_controller import ApplicationController

if __name__ == "__main__":
	app = QApplication(sys.argv)
	controller = ApplicationController()
	controller.run()
	sys.exit(app.exec_())

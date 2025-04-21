# main.py

import sys
from PyQt5.QtWidgets import QApplication
from UI.views.main_window import AttendixApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AttendixApp()
    window.show()
    sys.exit(app.exec_())

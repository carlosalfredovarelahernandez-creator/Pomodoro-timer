import sys
import os

# Esto asegura que Python pueda importar tus carpetas sin importar desde dónde lo ejecutes
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5.QtWidgets import QApplication
from ui.main_window import PomodoroApp

def run():
    app = QApplication(sys.argv)
    window = PomodoroApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()
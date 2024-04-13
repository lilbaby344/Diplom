import sys
from PyQt6.QtWidgets import QApplication, QDialog
from PyQt6 import uic


class MyDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('.ui/izd.ui', self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = MyDialog()
    dialog.show()
    sys.exit(app.exec())

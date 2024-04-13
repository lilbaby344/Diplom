import sys
from PyQt6.QtWidgets import QApplication, QDialog
from PyQt6 import uic
# from login import LoginDialog


class MyDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('.ui/lk.ui', self)

    #      # Привязка события к кнопке "Выйти"
    #     self.ui.pushButton.clicked.connect(self.logout)
    #
    # def logout(self):
    #     login_dialog = LoginDialog()
    #     login_dialog.show()
    #     self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = MyDialog()
    dialog.show()
    sys.exit(app.exec())

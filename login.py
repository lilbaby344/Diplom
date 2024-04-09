import sys
from PyQt6.QtWidgets import QApplication, QDialog
from PyQt6 import uic


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('.ui/login.ui', self)

        # Привязка событий кнопок
        self.ui.registerButton.setText("Зарегистрироваться")
        self.ui.loginButton.setText("Войти")
        self.ui.reg.setText("Нет аккаунта?")
        self.ui.vhod.setText("Авторизация")

        self.ui.registerButton.clicked.connect(self.register)
        self.ui.loginButton.clicked.connect(self.login)

    def register(self):
        username = self.ui.usernameLineEdit.text()
        password = self.ui.passwordLineEdit.text()
        print(f"Регистрация: {username}, {password}")

    def login(self):
        username = self.ui.usernameLineEdit.text()
        password = self.ui.passwordLineEdit.text()
        print(f"Вход: {username}, {password}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = LoginDialog()
    dialog.show()
    sys.exit(app.exec())

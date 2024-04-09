import sys
import subprocess
from PyQt6.QtWidgets import QApplication, QDialog


# Конвертация .ui файла в .py
def convert_ui_to_py(ui_file, py_file):
    try:
        subprocess.run(["pyuic6", "-x", ui_file, "-o", py_file], check=True)
        print(f"Файл {ui_file} успешно конвертирован в {py_file}")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при конвертации файла: {e}")

# Конвертируем перед запуском приложения
ui_file = "login.ui"
py_file = "login.py"
convert_ui_to_py(ui_file, py_file)

# Импортируем UI из сконвертированного файла
from login import Ui_Dialog

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # Привязка событий кнопок
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

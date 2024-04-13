import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt6.QtGui import QPixmap, QPalette, QBrush
from PyQt6 import uic
from lk import MyDialog

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('.ui/login.ui', self)

        self.setBackground('1.png')

        # Привязка событий кнопок
        self.ui.loginButton.setText("Войти")
        self.ui.vhod.setText("Авторизация")

        self.vhod.setStyleSheet("font-size: 20pt;")

        self.ui.loginButton.clicked.connect(self.login)
        self.ui.passwordLineEdit.returnPressed.connect(self.ui.loginButton.click)

    def setBackground(self, imagePath):
        pixmap = QPixmap(imagePath)
        brush = QBrush(pixmap)
        palette = QPalette()
        palette.setBrush(QPalette.ColorRole.Window, brush)
        self.setPalette(palette)

    def register(self):
        username = self.ui.usernameLineEdit.text()
        password = self.ui.passwordLineEdit.text()
        print(f"Регистрация: {username}, {password}")

    def login(self):
        username = self.ui.usernameLineEdit.text()
        password = self.ui.passwordLineEdit.text()

        conn = sqlite3.connect('diplom.db')
        cursor = conn.cursor()

        query = "SELECT * FROM пользователи WHERE табельныйНомер = ? AND пароль = ?"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()

        # Проверка результата запроса
        if result:
            print(f"Вход: {username}, {password}")
            self.lk_window = MyDialog()
            self.lk_window.show()
            self.close()

        else:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Ошибка")
            msg_box.setText("Ошибка авторизации. Попробуйте еще раз или обратитесь к системному администратору.")
            msg_box.setIcon(QMessageBox.CriticalIcon)
            msg_box.exec()
        conn.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = LoginDialog()
    dialog.show()
    sys.exit(app.exec())

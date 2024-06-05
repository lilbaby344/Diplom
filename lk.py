import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt6 import uic
# добавить фотки из бд, в файле бд фотки уже есть

def get_user_by_username_and_password(username, password):
    try:
        conn = sqlite3.connect('diplom.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM пользователи WHERE табельныйНомер=? AND пароль=?
        ''', (username, password))

        user = cursor.fetchone()
        conn.close()
        return user
    except sqlite3.Error as e:
        print(f"Ошибка при подключении к базе данных: {e}")
        return None

class MyDialog(QDialog):
    def __init__(self, username, password):
        super().__init__()
        self.ui = uic.loadUi('.ui/lk.ui', self)

        user = get_user_by_username_and_password(username, password)
        if user is not None:
            self.ui.FioLine.setText(user[1])
            self.ui.DolzhnostLine.setText(user[2])
            self.ui.OtdelLine.setText(user[3])
            self.ui.EmailLine.setText(user[4])
            self.ui.PhoneLine.setText(user[5])
            self.ui.TabnumLine.setText(user[6])
        else:
            QMessageBox.critical(self, "Ошибка", "Пользователь не найден")

        self.ui.pushButton.clicked.connect(self.logout)

        # Применение стилей
        self.apply_styles()

    def logout(self):
        from login import LoginDialog
        login_dialog = LoginDialog()
        login_dialog.show()
        self.close()

    def apply_styles(self):
        style_sheet = """
        QDialog {
            background-color: #e0f7fa; /* Светло-голубой фон */
        }
        QPushButton {
            background-color: #4fc3f7; /* Голубой цвет кнопки */
            color: white;
            border: none;
            border-radius: 10px; /* Закругленные углы */
            padding: 10px;
        }
        QPushButton:hover {
            background-color: #29b6f6; /* Цвет кнопки при наведении */
        }
        QLineEdit {
            border: 2px solid #4fc3f7;
            padding: 5px;
            border-radius: 5px;
        }
        QLabel {
            color: #01579b; /* Темно-синий цвет текста */
        }
        """
        self.setStyleSheet(style_sheet)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = MyDialog('username', 'password')
    dialog.show()
    sys.exit(app.exec())

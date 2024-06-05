import sys
from PyQt6.QtWidgets import QApplication
from login import LoginDialog

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Создаем экземпляр окна входа
    login_dialog = LoginDialog()

    # Отображаем окно входа
    login_dialog.show()

    sys.exit(app.exec())
# вызвать создание бд потом надежность
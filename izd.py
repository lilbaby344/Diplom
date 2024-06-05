import sys
from PyQt6.QtWidgets import QApplication, QDialog
from PyQt6 import uic


class MyDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('.ui/izd.ui', self)
        self.apply_styles()  # Применяем стили

    def apply_styles(self):
        style_sheet = """
        QDialog {
            background-color: #e0f7fa; /* Светло-голубой фон */
        }
        QLabel {
            color: #01579b; /* Темно-синий цвет текста */
        }
        QCommandLinkButton {
            background-color: #4fc3f7; /* Голубой цвет кнопки */
            color: white;
            border: none;
            border-radius: 10px; /* Закругленные углы */
            padding: 10px;
        }
        QCommandLinkButton:hover {
            background-color: #29b6f6; /* Цвет кнопки при наведении */
        }
        QProgressBar {
            border: 2px solid #4fc3f7;
            border-radius: 5px;
            text-align: center;
        }
        QProgressBar::chunk {
            background-color: #29b6f6;
        }
        """
        self.setStyleSheet(style_sheet)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = MyDialog()
    dialog.show()
    sys.exit(app.exec())

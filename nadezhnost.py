import sys
from PyQt6.QtWidgets import QApplication, QDialog
from PyQt6 import uic
import sqlite3

class nadezhnost(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('.ui/nadezhnost.ui', self)
        self.apply_styles()
        self.load_data()

    def apply_styles(self):
        # Применяем стили к элементам интерфейса
        button_style = """
        QPushButton {
            background-color: #4da6ff;
            color: white;
            border-radius: 10px;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #3399ff;
        }
        QPushButton:pressed {
            background-color: #007acc;
        }
        """

        combobox_style = """
        QComboBox {
            background-color: #ffffff;
            border: 1px solid #4da6ff;
            border-radius: 5px;
            padding: 3px;
        }
        QComboBox:hover {
            border: 1px solid #3399ff;
        }
        """

        lineedit_style = """
        QLineEdit {
            background-color: #ffffff;
            border: 1px solid #4da6ff;
            border-radius: 5px;
            padding: 3px;
        }
        QLineEdit:hover {
            border: 1px solid #3399ff;
        }
        """

        label_style = """
        QLabel {
            font-weight: bold;
        }
        """

        background_style = """
        QDialog {
            background-color: #e0f7fa;
        }
        """

        self.setStyleSheet(button_style + combobox_style + lineedit_style + label_style + background_style)

    def load_data(self):
        conn = sqlite3.connect('diplom.db')  # подключение к базе данных
        cursor = conn.cursor()

        query = "SELECT * FROM данные WHERE id=?"
        id = 1  # сделать айди динамически изменяемыми. Как не записывать сто раз одно и тоже в бд...
        cursor.execute(query, (id,))
        result = cursor.fetchone()

        if result is not None:
            id, ла, система, ки, описание, разработчик_интенсивность, эксплуатационная_интенсивность, стандарт_интенсивность, \
                уникальная_функция, функциональный_отказ, ссылка, dal, метод_контроля = result

            self.ui.comboBoxLA_2.setCurrentText(ла)
            self.ui.comboBoxSystem_2.setCurrentText(система)
            self.ui.lineEditKI_2.setText(ки)
            self.ui.lineEditOpisanie_2.setText(описание)
            self.ui.lineEditRazrab_2.setText(разработчик_интенсивность)
            self.ui.lineEditExp_2.setText(эксплуатационная_интенсивность)
            self.ui.lineEditStandart_2.setText(стандарт_интенсивность)
            self.ui.ButtonPlusFunction_3.setText(уникальная_функция)
            self.ui.ButtonPlusOtkaz_3.setText(функциональный_отказ)
            self.ui.comboBoxFdalIdal_2.setCurrentText(dal)
            self.ui.comboBoxMetod_2.setCurrentText(метод_контроля)

        conn.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = nadezhnost()
    dialog.show()
    sys.exit(app.exec())

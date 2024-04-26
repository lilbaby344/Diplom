import sys
from PyQt6.QtWidgets import QApplication, QDialog
from PyQt6 import uic
import sqlite3

class nadezhnost(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('.ui/nadezhnost.ui', self)
        self.load_data()

    def load_data(self):
        conn = sqlite3.connect('diplom.db')  # подключение к базе данных
        cursor = conn.cursor()

        query = "SELECT * FROM данные WHERE id=?"
        id = 8 #сделать айди динамически изменяемыми. Как не записывать сто раз одно и тоже в бд...
        cursor.execute(query, (id,))
        result = cursor.fetchone()

        if result is not None:
            id, ла, система, ки, описание, разработчик_интенсивность, эксплуатационная_интенсивность, стандарт_интенсивность, \
                уникальная_функция, функциональный_отказ, ссылка, dal, метод_контроля = result

            # здесь вы можете присвоить эти значения вашим полям в интерфейсе
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

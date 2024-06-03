import sqlite3
import sys
from PyQt6.QtWidgets import QApplication, QDialog
from PyQt6 import uic


def create_connection():
    try:
        conn = sqlite3.connect('diplom.db')
        return conn
    except sqlite3.Error as e:
        print(e)
        return None


def create_tables():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS данные (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ЛА TEXT,
                Система TEXT,
                КИ TEXT,
                Описание TEXT,
                Разработчик_Интенсивность TEXT,
                Эксплуатационная_Интенсивность TEXT,
                Стандарт_Интенсивность TEXT,
                Уникальная_Функция TEXT,
                Функциональный_Отказ TEXT,
                Ссылка TEXT,
                DAL TEXT,
                Метод_контроля TEXT,
                UNIQUE(ЛА, Система, КИ, Описание)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS пользователи (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ФИО TEXT,
                Должность TEXT,
                Отдел TEXT,
                Почта TEXT,
                НомерТелефона TEXT,
                табельныйНомер TEXT,
                пароль TEXT,
                фото BLOB,
                UNIQUE(табельныйНомер)
            )
        ''')

        conn.commit()
        conn.close()


def load_photo_as_blob(file_path):
    with open(file_path, 'rb') as file:
        blob = file.read()
    return blob


def insert_data_into_данные(ла, система, ки, описание, разработчик_интенсивность, эксплуатационная_интенсивность,
                            стандарт_интенсивность, уникальная_функция, функциональный_отказ, ссылка, dal,
                            метод_контроля):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()

        # Проверка на существование записи
        cursor.execute('''
            SELECT * FROM данные WHERE ЛА = ? AND Система = ? AND КИ = ? AND Описание = ?
        ''', (ла, система, ки, описание))
        if cursor.fetchone() is None:
            cursor.execute('''
                INSERT INTO данные (ЛА, Система, КИ, Описание, Разработчик_Интенсивность, Эксплуатационная_Интенсивность, Стандарт_Интенсивность, Уникальная_Функция, Функциональный_Отказ, Ссылка, DAL, Метод_контроля)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                ла, система, ки, описание, разработчик_интенсивность, эксплуатационная_интенсивность, стандарт_интенсивность,
                уникальная_функция, функциональный_отказ, ссылка, dal, метод_контроля))

        conn.commit()
        conn.close()


def insert_user(фио, должность, отдел, табельныйНомер, почта, номерТелефона, пароль, фото):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()

        # Проверка на существование пользователя по табельному номеру
        cursor.execute('''
            SELECT * FROM пользователи WHERE табельныйНомер = ?
        ''', (табельныйНомер,))
        if cursor.fetchone() is None:
            cursor.execute('''
                INSERT INTO пользователи (ФИО, Должность, Отдел, табельныйНомер, Почта, НомерТелефона, пароль, фото)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (фио, должность, отдел, табельныйНомер, почта, номерТелефона, пароль, фото))

        conn.commit()
        conn.close()


if __name__ == "__main__":
    create_tables()

    # Добавление данных в таблицу данные
    insert_data_into_данные('Boeing 737', 'Навигационная система', 'КИ1', 'Высокая', 'Разработчик_Интенсивность1',
                            'Эксплуатационная_Интенсивность1', 'Стандарт_Интенсивность1', 'Уникальная_Функция1',
                            'Функциональный_Отказ1', 'Ссылка1', 'DAL1', 'Метод_контроля1')
    insert_data_into_данные('Airbus A320', 'Топливная система', 'КИ2', 'Средняя', 'Разработчик_Интенсивность2',
                            'Эксплуатационная_Интенсивность2', 'Стандарт_Интенсивность2', 'Уникальная_Функция2',
                            'Функциональный_Отказ2', 'Ссылка2', 'DAL2', 'Метод_контроля2')
    # Добавление пользователей с фото
    path_to_photos = 'C:/Users/kuttu/PycharmProjects/diplom/photo/'

    insert_user('Куттумуратова Лаура Саматовна', 'Главный инженер', 'Отдел надежности', '1', 'kuttumuratovaa@mail.ru',
                '89325575423', '1', load_photo_as_blob(path_to_photos + 'laura.jpg'))
    insert_user('Иванов Иван Иванович', 'Инженер', 'Отдел разработки', '66666', 'ivanov@mail.ru', '89321112233',
                'password2', load_photo_as_blob(path_to_photos + 'photo2.jpg'))
    insert_user('Петрова Елена Сергеевна', 'Менеджер', 'Отдел продаж', '77777', 'petrova@mail.ru', '89323334455',
                'password3', load_photo_as_blob(path_to_photos + 'photo3.jpg'))
    insert_user('Сидоров Сергей Алексеевич', 'Тестировщик', 'Отдел тестирования', '88888', 'sidorov@mail.ru', '89324445566',
                'password4', load_photo_as_blob(path_to_photos + 'photo4.jpg'))
    insert_user('Кузнецова Наталья Владимировна', 'Бухгалтер', 'Бухгалтерия', '99999', 'kuznetsova@mail.ru', '89326667788',
                'password5', load_photo_as_blob(path_to_photos + 'photo5.jpg'))
    insert_user('Александров Александр Александрович', 'Директор', 'Дирекция', '00000', 'alexandrov@mail.ru', '89327778899',
                'password6', load_photo_as_blob(path_to_photos + 'photo6.jpg'))

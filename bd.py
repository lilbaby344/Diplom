import sqlite3
import sys
from PyQt6.QtWidgets import QApplication, QDialog
from PyQt6.QtGui import QPixmap, QPalette, QBrush
from PyQt6 import uic

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('diplom.db')
    except sqlite3.Error as e:
        print(e)
    return conn

def create_tables():
    conn = create_connection()
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
            Метод_контроля TEXT
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
            пароль TEXT
        )
    ''')

    conn.commit()
    conn.close()

def insert_data_into_данные(ла, система, ки, описание, разработчик_интенсивность, эксплуатационная_интенсивность, стандарт_интенсивность, уникальная_функция, функциональный_отказ, ссылка, dal, метод_контроля):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO данные (ЛА, Система, КИ, Описание, Разработчик_Интенсивность, Эксплуатационная_Интенсивность, Стандарт_Интенсивность, Уникальная_Функция, Функциональный_Отказ, Ссылка, DAL, Метод_контроля)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (ла, система, ки, описание, разработчик_интенсивность, эксплуатационная_интенсивность, стандарт_интенсивность, уникальная_функция, функциональный_отказ, ссылка, dal, метод_контроля))

    conn.commit()
    conn.close()

def insert_user(фио, должность, отдел, табельныйНомер, почта, номерТелефона, пароль):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO пользователи (ФИО, Должность, Отдел, табельныйНомер, Почта, НомерТелефона, пароль)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (фио, должность, отдел, табельныйНомер, почта, номерТелефона, пароль))

    conn.commit()
    conn.close()

create_tables()

insert_data_into_данные('ЛА1', 'Система1', 'КИ1', 'Описание1', 'Разработчик_Интенсивность1', 'Эксплуатационная_Интенсивность1', 'Стандарт_Интенсивность1', 'Уникальная_Функция1', 'Функциональный_Отказ1', 'Ссылка1', 'DAL1', 'Метод_контроля1')
insert_data_into_данные('ЛА2', 'Система2', 'КИ2', 'Описание2', 'Разработчик_Интенсивность2', 'Эксплуатационная_Интенсивность2', 'Стандарт_Интенсивность2', 'Уникальная_Функция2', 'Функциональный_Отказ2', 'Ссылка2', 'DAL2', 'Метод_контроля2')

insert_user('Куттумуратова Лаура Саматовна', 'Главный инженер', 'Отдел надежности', '1', 'kuttumuratovaa@mail.ru', '89325575423', '1')
insert_user('Иванов Иван Иванович', 'Инженер', 'Отдел разработки', '66666', 'ivanov@mail.ru', '89321112233', 'password2')
insert_user('Петрова Елена Сергеевна', 'Менеджер', 'Отдел продаж', '77777', 'petrova@mail.ru', '89323334455', 'password3')
insert_user('Сидоров Сергей Алексеевич', 'Тестировщик', 'Отдел тестирования', '88888', 'sidorov@mail.ru', '89324445566', 'password4')
insert_user('Кузнецова Наталья Владимировна', 'Бухгалтер', 'Бухгалтерия', '99999', 'kuznetsova@mail.ru', '89326667788', 'password5')
insert_user('Александров Александр Александрович', 'Директор', 'Дирекция', '00000', 'alexandrov@mail.ru', '89327778899', 'password6')


def login(username, password):
    conn = create_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM users WHERE username=? AND password=?"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()


#таблица пользоватеи заполнение


    conn.close()

    return user is not None


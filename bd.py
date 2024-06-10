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
                табельныйНомер TEXT UNIQUE,
                пароль TEXT,
                фото BLOB,
                роль_id INTEGER,
                FOREIGN KEY (роль_id) REFERENCES роли(id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS роли (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                название TEXT UNIQUE,
                права TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS отделы (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                название TEXT UNIQUE
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS проекты (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                название TEXT,
                описание TEXT,
                дата_начала DATE,
                дата_окончания DATE,
                руководитель INTEGER,
                FOREIGN KEY (руководитель) REFERENCES пользователи(id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS задачи (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                название TEXT,
                описание TEXT,
                дата_начала DATE,
                дата_окончания DATE,
                статус TEXT,
                проект_id INTEGER,
                ответственный INTEGER,
                FOREIGN KEY (проект_id) REFERENCES проекты(id),
                FOREIGN KEY (ответственный) REFERENCES пользователи(id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS самолеты (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                название TEXT,
                модель TEXT,
                производитель TEXT,
                серийный_номер TEXT UNIQUE
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS системы (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                название TEXT,
                описание TEXT,
                самолет_id INTEGER,
                FOREIGN KEY (самолет_id) REFERENCES самолеты(id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS отказы (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                описание TEXT,
                дата DATE,
                система_id INTEGER,
                пользователь_id INTEGER,
                FOREIGN KEY (система_id) REFERENCES системы(id),
                FOREIGN KEY (пользователь_id) REFERENCES пользователи(id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS логи (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                действие TEXT,
                дата DATE,
                пользователь_id INTEGER,
                FOREIGN KEY (пользователь_id) REFERENCES пользователи(id)
            )
        ''')

        # Добавление ролей
        cursor.execute('''
            INSERT OR IGNORE INTO роли (название, права) VALUES
            ('Суперпользователь', 'чтение, запись, удаление'),
            ('Менеджер', 'чтение')
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


def insert_user(фио, должность, отдел, табельныйНомер, почта, номерТелефона, пароль, фото, роль):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()

        # Получение id роли
        cursor.execute('''
            SELECT id FROM роли WHERE название = ?
        ''', (роль,))
        роль_id = cursor.fetchone()[0]

        # Проверка на существование пользователя по табельному номеру
        cursor.execute('''
            SELECT * FROM пользователи WHERE табельныйНомер = ?
        ''', (табельныйНомер,))
        if cursor.fetchone() is None:
            cursor.execute('''
                INSERT INTO пользователи (ФИО, Должность, Отдел, табельныйНомер, Почта, НомерТелефона, пароль, фото, роль_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (фио, должность, отдел, табельныйНомер, почта, номерТелефона, пароль, фото, роль_id))

        conn.commit()
        conn.close()


def insert_самолет(название, модель, производитель, серийный_номер):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO самолеты (название, модель, производитель, серийный_номер)
            VALUES (?, ?, ?, ?)
        ''', (название, модель, производитель, серийный_номер))

        conn.commit()
        conn.close()


def insert_система(название, описание, самолет_id):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO системы (название, описание, самолет_id)
            VALUES (?, ?, ?)
        ''', (название, описание, самолет_id))

        conn.commit()
        conn.close()


def insert_отказ(описание, дата, система_id, пользователь_id):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO отказы (описание, дата, система_id, пользователь_id)
            VALUES (?, ?, ?, ?)
        ''', (описание, дата, система_id, пользователь_id))

        conn.commit()
        conn.close()


def insert_лог(действие, дата, пользователь_id):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO логи (действие, дата, пользователь_id)
            VALUES (?, ?, ?)
        ''', (действие, дата, пользователь_id))

        conn.commit()
        conn.close()


if __name__ == "__main__":
    create_tables()

    # Примеры данных для таблицы "данные"
    insert_data_into_данные('Boeing 737', 'Навигационная система', 'КИ1', 'Описание системы навигации', 'Высокая',
                            'Средняя', 'Стандартная', 'Функция навигации', 'Отказ навигации', 'www.link1.com', 'DAL A',
                            'Метод контроля 1')
    insert_data_into_данные('Airbus A320', 'Топливная система', 'КИ2', 'Описание топливной системы', 'Средняя',
                            'Низкая', 'Высокая', 'Функция подачи топлива', 'Отказ подачи топлива', 'www.link2.com', 'DAL B',
                            'Метод контроля 2')
    insert_data_into_данные('Boeing 747', 'Гидравлическая система', 'КИ3', 'Описание гидравлической системы', 'Низкая',
                            'Высокая', 'Стандартная', 'Функция гидравлики', 'Отказ гидравлики', 'www.link3.com', 'DAL C',
                            'Метод контроля 3')
    insert_data_into_данные('Airbus A380', 'Электрическая система', 'КИ4', 'Описание электрической системы', 'Высокая',
                            'Средняя', 'Низкая', 'Функция электропитания', 'Отказ электропитания', 'www.link4.com', 'DAL D',
                            'Метод контроля 4')
    insert_data_into_данные('Boeing 787', 'Система жизнеобеспечения', 'КИ5', 'Описание системы жизнеобеспечения', 'Средняя',
                            'Высокая', 'Стандартная', 'Функция жизнеобеспечения', 'Отказ жизнеобеспечения', 'www.link5.com', 'DAL E',
                            'Метод контроля 5')
    insert_data_into_данные('Airbus A330', 'Система связи', 'КИ6', 'Описание системы связи', 'Низкая',
                            'Средняя', 'Высокая', 'Функция связи', 'Отказ связи', 'www.link6.com', 'DAL F',
                            'Метод контроля 6')

    # Добавление пользователей с фото и ролями
    path_to_photos = 'C:/Users/kuttu/PycharmProjects/diplom/photo/'

    insert_user('Куттумуратова Лаура Саматовна', 'Главный инженер', 'Отдел надежности', '1', 'kuttumuratovaa@mail.ru',
                '89325575423', '1', load_photo_as_blob(path_to_photos + 'laura.jpg'), 'Суперпользователь')
    insert_user('Иванов Иван Иванович', 'Инженер', 'Отдел разработки', '66666', 'ivanov@mail.ru', '89321112233',
                'password2', load_photo_as_blob(path_to_photos + 'photo2.jpg'), 'Менеджер')
    insert_user('Петрова Елена Сергеевна', 'Менеджер', 'Отдел продаж', '77777', 'petrova@mail.ru', '89323334455',
                'password3', load_photo_as_blob(path_to_photos + 'photo3.jpg'), 'Менеджер')
    insert_user('Сидоров Сергей Алексеевич', 'Тестировщик', 'Отдел тестирования', '88888', 'sidorov@mail.ru', '89324445566',
                'password4', load_photo_as_blob(path_to_photos + 'photo4.jpg'), 'Менеджер')
    insert_user('Кузнецова Наталья Владимировна', 'Бухгалтер', 'Бухгалтерия', '99999', 'kuznetsova@mail.ru', '89326667788',
                'password5', load_photo_as_blob(path_to_photos + 'photo5.jpg'), 'Менеджер')
    insert_user('Александров Александр Александрович', 'Директор', 'Дирекция', '00000', 'alexandrov@mail.ru', '89327778899',
                'password6', load_photo_as_blob(path_to_photos + 'photo6.jpg'), 'Суперпользователь')

    # Примеры данных для таблицы "самолеты"
    insert_самолет('Boeing 737', '737-800', 'Boeing', 'SN001')
    insert_самолет('Airbus A320', 'A320-200', 'Airbus', 'SN002')
    insert_самолет('Boeing 747', '747-400', 'Boeing', 'SN003')
    insert_самолет('Airbus A380', 'A380-800', 'Airbus', 'SN004')
    insert_самолет('Boeing 787', '787-9', 'Boeing', 'SN005')
    insert_самолет('Airbus A330', 'A330-300', 'Airbus', 'SN006')

    # Примеры данных для таблицы "системы"
    insert_система('Навигационная система', 'Система навигации для точного ведения маршрута', 1)
    insert_система('Топливная система', 'Система подачи и хранения топлива', 2)
    insert_система('Гидравлическая система', 'Система гидравлики для управления элементами самолета', 3)
    insert_система('Электрическая система', 'Система электропитания самолета', 4)
    insert_система('Система жизнеобеспечения', 'Система жизнеобеспечения для пассажиров и экипажа', 5)
    insert_система('Система связи', 'Система связи для внутренней и внешней коммуникации', 6)

    # Примеры данных для таблицы "отказы"
    insert_отказ('Ошибка навигации', '2024-06-01', 1, 1)
    insert_отказ('Утечка топлива', '2024-06-02', 2, 2)
    insert_отказ('Потеря давления в гидравлике', '2024-06-03', 3, 3)
    insert_отказ('Сбой в электропитании', '2024-06-04', 4, 4)
    insert_отказ('Неисправность системы жизнеобеспечения', '2024-06-05', 5, 5)
    insert_отказ('Проблемы со связью', '2024-06-06', 6, 6)

    # Примеры данных для таблицы "логи"
    insert_лог('Вход в систему', '2024-06-01', 1)
    insert_лог('Добавление данных', '2024-06-02', 2)
    insert_лог('Обновление записи', '2024-06-03', 3)
    insert_лог('Удаление записи', '2024-06-04', 4)
    insert_лог('Выход из системы', '2024-06-05', 5)
    insert_лог('Просмотр данных', '2024-06-06', 6)
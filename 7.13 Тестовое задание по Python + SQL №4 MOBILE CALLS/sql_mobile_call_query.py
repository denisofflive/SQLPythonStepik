import csv
import os
import random
import sqlite3
from datetime import datetime


class SQLMobileCallsQuery:
    """Создание таблица mobile_users"""
    MOBILE_CALLS_DB = "mobile_calls.db"
    REPORT_CSV = 'report_mobile.csv'

    def get_path_to_mobile_calls_db(self):
        return os.path.join(self.BASE_DIR, self.MOBILE_CALLS_DB)

    def __init__(self, base_dir):
        self.BASE_DIR = base_dir
        self.create_table_mobile_users()
        self.create_table_mobile_price()

    @staticmethod
    def generate_now_date():
        return datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    def create_table_mobile_users(self):
        """Создание таблицы: mobile_users"""
        path_to_db = self.get_path_to_mobile_calls_db()
        with sqlite3.connect(path_to_db) as db:
            cur = db.cursor()
            cur.execute('''
            CREATE TABLE IF NOT EXISTS mobile_users(
            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
            User VARCHAR(255) NOT NULL,
            Balance INTEGER NOT NULL);''')
            db.commit()
            print("Создание таблицы mobile_users.")

    def create_table_mobile_price(self):
        """Создание таблицы: mobile_users"""
        path_to_db = self.get_path_to_mobile_calls_db()
        with sqlite3.connect(path_to_db) as db:
            cur = db.cursor()
            cur.execute('''
                CREATE TABLE IF NOT EXISTS mobile_price(
                PriceID INTEGER PRIMARY KEY AUTOINCREMENT,
                Mts_Mts INTEGER NOT NULL,
                Mts_Tele2 INTEGER NOT NULL,
                Mts_Yota INTEGER NOT NULL);''')
            db.commit()
            print("Создание таблицы mobile_price.")

    def insert_user_data(self, data_user):
        """Добавление пользователя в таблицу mobile_users data_user = (str, int)"""
        path_to_db = self.get_path_to_mobile_calls_db()
        with sqlite3.connect(path_to_db) as db:
            cur = db.cursor()
            cur.execute('''
                INSERT INTO mobile_users (User, Balance)
                VALUES (?, ?);''', data_user)
            print(f'Добавление пользователя: {data_user}.')

    def insert_price_data(self, data_tariff):
        """Добавление тарифа в таблицу mobile_price data_tariff = (int, int, int)"""
        path_to_db = self.get_path_to_mobile_calls_db()
        with sqlite3.connect(path_to_db) as db:
            cur = db.cursor()
            cur.execute('''
                    INSERT INTO mobile_price (Mts_Mts, Mts_Tele2, Mts_Yota)
                    VALUES (?, ?, ?);''', data_tariff)
            print(f'Добавление тарифа: {data_tariff}.')

    def generate_report_mobile(self):
        """Отчет об операциях
        Type_operation:
        1 = Mts_Mts
        2 = Mts_Tele2
        3 = Mts_Yota
        """
        user_data = [
            ('Date', 'Operator', 'Count_min', 'Amount')
        ]
        path_to_csv = os.path.join(self.BASE_DIR, self.REPORT_CSV)
        with open(path_to_csv, 'a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerows(
                user_data
            )
        print(f'Создан отчет: report_mobile.csv.Сохранен по пути: {path_to_csv}')

    def add_data_to_report_mobile(self, date, operator, minute, amount):
        user_data = [
            (date, operator, minute, amount)
        ]
        path_to_csv = os.path.join(self.BASE_DIR, self.REPORT_CSV)
        with open(path_to_csv, 'a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerows(
                user_data
            )
        print('Данные были добавлены в : report_mobile.csv. Сохранен по пути: {path_to_csv}')

    def cycle(self):
        path_to_db = self.get_path_to_mobile_calls_db()
        with sqlite3.connect(path_to_db) as db:
            cur = db.cursor()
            cur.execute('''
            SELECT Mts_Mts, Mts_Tele2, Mts_Yota FROM mobile_price''')
            operators_id = cur.fetchone()
            count = 30
            while count != 0:
                operator = {1: 'Mts_Mts', 2: 'Mts_Tele2', 3: 'Mts_Yota'}
                random_operator = random.choice(operators_id)
                random_minute = random.randint(1, 10)
                cur.execute('''
                SELECT Balance FROM mobile_users''')
                user_balance = cur.fetchone()
                amount = random_operator * random_minute
                if user_balance[0] > 0 and (user_balance[0] - amount) > 0:
                    cur.execute(f'''
                    UPDATE mobile_users
                    SET Balance = Balance - {amount};''')
                    db.commit()
                    now_date = self.generate_now_date()
                    self.add_data_to_report_mobile(now_date, operator.get(random_operator), random_minute, amount)
                    count -= 1
                    cur.execute('''
                            SELECT Balance FROM mobile_users''')
                    final_balance = cur.fetchone()
                    print('Оператор: ', operator.get(random_operator), '.', 'Минут: ',
                          random_minute, '.', 'Сумма: ', amount, '.', 'Баланс пользователя: ', final_balance[0], '.')
                else:
                    print('Баланс пользователя:', user_balance[0])
                    print('У пользователя недостаточно средств!')
                    return False

        cur.execute('''
        SELECT Balance FROM mobile_users''')
        final_balance = cur.fetchone()
        print('Итоговый баланс:', final_balance[0])


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    mobile_calls = SQLMobileCallsQuery(BASE_DIR)
    mobile_calls.generate_report_mobile()

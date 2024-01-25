import csv
import random
import sqlite3

from datetime import datetime

now_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class SQLMobileCallsQuery:

    """Создание таблица mobile_users"""

    @staticmethod
    def create_table_mobile_users():

        with sqlite3.connect('mobile_calls.db') as db:
            cur = db.cursor()
            cur.execute('''
            CREATE TABLE IF NOT EXISTS mobile_users(
            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
            User VARCHAR(255) NOT NULL,
            Balance INTEGER NOT NULL);''')
            print("Создание таблицы mobile_users.")

    """Создание таблицы: mobile_price"""

    @staticmethod
    def create_table_mobile_price():

        with sqlite3.connect('mobile_calls.db') as db:
            cur = db.cursor()
            cur.execute('''
                CREATE TABLE IF NOT EXISTS mobile_price(
                PriceID INTEGER PRIMARY KEY AUTOINCREMENT,
                Mts_Mts INTEGER NOT NULL,
                Mts_Tele2 INTEGER NOT NULL,
                Mts_Yota INTEGER NOT NULL);''')
            print("Создание таблицы mobile_price.")

    """Добавление пользователя в таблицу mobile_users

        data_user = (str, int)"""
    @staticmethod
    def insert_user(data_user):

        with sqlite3.connect('mobile_calls.db') as db:
            cur = db.cursor()
            cur.execute('''
                INSERT INTO mobile_users (User, Balance)
                VALUES (?, ?);''', data_user)
            print(f'Добавление пользователя: {data_user}.')

    """Добавление тарифа в таблицу mobile_price

        data_tariff = (int, int, int)"""
    @staticmethod
    def insert_price(data_tariff):
        with sqlite3.connect('mobile_calls.db') as db:
            cur = db.cursor()
            cur.execute('''
                    INSERT INTO mobile_price (Mts_Mts, Mts_Tele2, Mts_Yota)
                    VALUES (?, ?, ?);''', data_tariff)
            print(f'Добавление тарифа: {data_tariff}.')

    """Отчет об операциях
        
        Type_operation:
        1 = Mts_Mts
        2 = Mts_Tele2
        3 = Mts_Yota
        """

    @staticmethod
    def create_report_mobile():

        user_data = [
            ('Date', 'Operator', 'Count_min', 'Amount')
        ]
        with open('report_mobile.csv', 'a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerows(
                user_data
            )
        print('Создан отчет: report_mobile.csv')

    @staticmethod
    def added_data_to_report_mobile(date, operator, minute, amount):
        user_data = [
            (date, operator, minute, amount)
        ]
        with open('report_mobile.csv', 'a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerows(
                user_data
            )
        print('Данные были добавлены в : report_mobile.csv')

    @staticmethod
    def cycle():

        with sqlite3.connect('mobile_calls.db') as db:
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
                    SQLMobileCallsQuery.added_data_to_report_mobile(
                        now_date, operator.get(random_operator), random_minute, amount)
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

SQLMobileCallsQuery.create_report_mobile()

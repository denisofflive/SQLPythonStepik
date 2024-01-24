import sqlite3


class SQL_mobile:
    """Создание таблиц"""

    @staticmethod
    def create_table():
        with sqlite3.connect('mobile.db') as db:
            cur = db.cursor()

            cur.execute("""CREATE TABLE IF NOT EXISTS mobile_users(
                UserID INTEGER PRIMARY KEY AUTOINCREMENT,
                User_name VARCHAR(255) NOT NULL,
                Balance INTEGER NOT NULL,
                Mobile_tariff_ref INTEGER NOT NULL,
                Activity VARCHAR(255) NOT NULL);""")
            print('Создание таблицы mobile_users')

            cur.execute("""CREATE TABLE IF NOT EXISTS mobile_tariff(
                TariffID INTEGER PRIMARY KEY AUTOINCREMENT,
                Tariff VARCHAR(255) NOT NULL, 
                Price INTEGER NOT NULL);""")
            db.commit()
            print('Создание таблицы mobile_tariff')

    """Заполнение таблицы mobile_users"""

    @staticmethod
    def insert_users(data_users):
        with sqlite3.connect("mobile.db") as db:
            cur = db.cursor()
            cur.execute(
                """INSERT INTO mobile_users (User_name, Balance, Mobile_tariff_ref, Activity) VALUES(?, ?, ?, ?);""",
                data_users)
            db.commit()
            print('Создание нового пользователя')

    """Заполнение таблицы mobile_tariff"""

    @staticmethod
    def insert_tariff(data_tariff):
        with sqlite3.connect("mobile.db") as db:
            cur = db.cursor()

            cur.execute(
                """INSERT INTO mobile_tariff (Tariff, Price) VALUES(?, ?);""",
                data_tariff)
            db.commit()
            print('Создание нового тарифа')

    """Количество активных пользователей"""

    @staticmethod
    def active_user():

        with sqlite3.connect("mobile.db") as db:
            cur = db.cursor()

            cur.execute(
                """SELECT UserID, User_name, Activity, Tariff, Price FROM mobile_users 
                INNER JOIN mobile_tariff ON TariffID = Mobile_tariff_ref;""")
            table_user = cur.fetchall()
            data_user = table_user
            db.commit()

            print('Активные пользователи:\n')

            for user in data_user:
                if user[2] == 'Yes':
                    print(f"Login - {user[1]}, " + f"Active - {user[2]}, " + f"Tariff - {user[3]}.")

    """Ежемесячная оплата тарифа"""

    @staticmethod
    def withdraw_money(period):

        if period == '0':
            print('Введён неверный период')
        else:

            with sqlite3.connect("mobile.db") as db:
                cur = db.cursor()
                # Объединённая таблица с тарифами, прайсом и балансом
                cur.execute(
                    """SELECT UserID, User_name, Balance, Activity, Tariff, Price FROM mobile_users 
                    INNER JOIN mobile_tariff ON TariffID = Mobile_tariff_ref;""")
                data_user = cur.fetchall()
                user = data_user

                try:
                    # Цикл для работы со всеми пользователями
                    for activity in user:

                        if activity[3] == 'No':
                            continue

                        # Изменение статуса пользователя
                        elif int(activity[2]) <= int(activity[5]):
                            cur.execute(f"""UPDATE mobile_users SET Activity='No' WHERE UserID={activity[0]};""")
                            db.commit()
                            print('Статус пользователя был изменён')

                        result = int(activity[5]) * int(
                            period)  # Переменная для расчёта количества нужной суммы за нужный период

                        if int(result) > int(activity[2]):  # Проверка на то, достаточно ли средств у пользователя
                            print('Недостаточно средств для совершения операции.')

                        else:

                            cur.execute(
                                f"""UPDATE mobile_users SET Balance= Balance-{result} WHERE UserID={activity[0]}""")

                            cur.execute(f"""SELECT Balance FROM mobile_users WHERE UserID={activity[0]}""")
                            data_balance = cur.fetchone()
                            balance_user = data_balance[0]
                            db.commit()
                            print(
                                f'Было списано с баланса пользователя {activity[1]} '
                                f'ежемесячная плата за установленный период. Баланс пользователя составляет -'
                                f' {balance_user}')
                except:
                    print('Попытка выполнить некорректное действие')

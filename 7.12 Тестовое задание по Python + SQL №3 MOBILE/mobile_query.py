import sqlite3


def create_tables(db, cur):
    print('Создаю таблицу mobile_users')
    cur.execute("""CREATE TABLE IF NOT EXISTS mobile_users(
        UserID INTEGER PRIMARY KEY AUTOINCREMENT,
        User_name VARCHAR(255) NOT NULL,
        Balance INTEGER NOT NULL,
        Mobile_tariff_ref INTEGER NOT NULL,
        Activity VARCHAR(255) NOT NULL);""")

    print('Создаю таблицу mobile_tariff')
    cur.execute("""CREATE TABLE IF NOT EXISTS mobile_tariff(
        TariffID INTEGER PRIMARY KEY AUTOINCREMENT,
        Tariff VARCHAR(255) NOT NULL, 
        Price INTEGER NOT NULL);""")
    db.commit()


def insert_users(db, cur, data_users):
    print(f'Создание нового пользователя с данными: {data_users}')
    cur.execute("""INSERT INTO mobile_users (User_name, Balance, Mobile_tariff_ref, Activity) VALUES(?, ?, ?, ?);""",
                data_users)
    db.commit()


def insert_tariff(db, cur, data_tariff):
    print(f'Создание нового тарифа c данными: {data_tariff}')
    cur.execute("""INSERT INTO mobile_tariff (Tariff, Price) VALUES(?, ?);""", data_tariff)
    db.commit()


def show_active_user(cur):
    cur.execute(
        """SELECT UserID, User_name, Activity, Tariff, Price FROM mobile_users INNER JOIN mobile_tariff ON TariffID = Mobile_tariff_ref;""")
    table_user = cur.fetchall()
    data_user = table_user
    print('Активные пользователи:\n')
    for user in data_user:
        if user[2] == 'Yes':
            print(f"Login - {user[1]}, " + f"Active - {user[2]}, " + f"Tariff - {user[3]}.")


def withdraw_money(db, cur, period):
    for num_p in range(1, period):
        cur.execute(
            """SELECT UserID, User_name, Balance, Activity, Tariff, Price FROM mobile_users 
                INNER JOIN mobile_tariff ON TariffID = Mobile_tariff_ref;""")
        active_users = cur.fetchall()
        for user in active_users:
            if user[3] == 'No':
                continue
            print(f"{user[1]} снятие денежных средств {user[5]} за месяц {num_p}")
            if int(user[2]) <= int(user[5]):
                print(f"{user[1]} недостаточно средств для совершения операции.Баланс: {user[2]}.Требуется: {user[5]}")
                cur.execute(f"""UPDATE mobile_users SET Activity='No' WHERE UserID={user[0]};""")
                db.commit()
            else:
                cur.execute(f"""UPDATE mobile_users SET Balance= Balance-{user[5]} WHERE UserID={user[0]}""")
                db.commit()
                cur.execute(f"""SELECT Balance FROM mobile_users WHERE UserID={user[0]}""")
                balance_user = cur.fetchone()[0]
                print(
                    f'Было списано с баланса пользователя {user[1]} '
                    f'ежемесячная плата за установленный период. Баланс пользователя составляет -'
                    f' {balance_user}')


if __name__ == "__main__":

    db = sqlite3.connect('mobile.db')
    cur = db.cursor()

    create_tables(db, cur)
    insert_users(db, cur, ('User1', 10000, 2, 'Yes'))
    insert_users(db, cur, ('User2', 10000, 3, 'Yes'))
    insert_users(db, cur, ('User3', 10000, 1, 'Yes'))
    insert_tariff(db, cur, ('Standard', 500))
    insert_tariff(db, cur, ('VIP', 1000))
    insert_tariff(db, cur, ('Premium', 1500))

    show_active_user(cur)

    period = input('\nВведите количество месяцев: ')
    if not period.isdigit() or float(period) < 0:
        print("Вы ввели неправильное кол-во месяцев")

    withdraw_money(db, cur, int(period))

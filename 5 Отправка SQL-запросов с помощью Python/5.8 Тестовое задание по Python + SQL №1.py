import sqlite3

# Создание базы данных
db = sqlite3.connect('registration.db')
cur = db.cursor()

# Создание таблицы users_data
cur.execute('''
    CREATE TABLE IF NOT EXISTS users_data (
        userid INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT UNIQUE,
        password TEXT,
        code INTEGER
    )
''')

db.commit()

# Функция для регистрации нового пользователя
def register_user():
    login = input("Введите логин: ")
    password = input("Введите пароль: ")
    code = int(input("Введите код (4-х значное целое число): "))

    try:
        cur.execute('''
            INSERT INTO users_data (login, password, code)
            VALUES (?, ?, ?)
        ''', (login, password, code))
        db.commit()
        print("Пользователь успешно зарегистрирован.")
    except sqlite3.IntegrityError:
        print("Пользователь с таким логином уже существует.")

# Функция для авторизации пользователя
def login_user():
    login = input("Введите логин: ")
    password = input("Введите пароль: ")

    cur.execute('''
        SELECT * FROM users_data
        WHERE login = ? AND password = ?
    ''', (login, password))

    user = cur.fetchone()

    if user:
        print("Авторизация успешна.")
    else:
        print("Неверный логин или пароль.")

# Функция для восстановления пароля
def recover_password():
    login = input("Введите логин: ")
    code = int(input("Введите код: "))
    new_password = input("Введите новый пароль: ")

    cur.execute('''
        UPDATE users_data
        SET password = ?
        WHERE login = ? AND code = ?
    ''', (new_password, login, code))
    db.commit()

    if cur.rowcount > 0:
        print("Пароль успешно изменен.")
    else:
        print("Неверный логин или код.")

# Пользовательский интерфейс
while True:
    print("Выберите действие:")
    print("1. Регистрация нового пользователя")
    print("2. Авторизация в системе")
    print("3. Восстановление пароля")
    print("0. Закрыть программу")

    choice = input("Введите номер действия: ")

    if choice == "1":
        register_user()
    elif choice == "2":
        login_user()
    elif choice == "3":
        recover_password()
    elif choice == "0":
        break
    else:
        print("Неверный выбор.")

# Закрытие программы
db.close()
import os
import sqlite3


def check_that_int():
    while True:
        print('Введите код:')
        try:
            num = int(input())
            return num
        except ValueError:
            print('Введите номер!')
            print('Попробуйте снова?')
            print('Выберите Y/N')
            answer = input()
            answer = answer.lower()
            if answer == 'y':
                continue
            else:
                print("Вы ввели неверные данные")
                break


def select_option():
    options_list = [1, 2, 3]
    while True:
        print(
            '\nВыберите действие:\n'
            ' \n1. Регистрация нового пользователя'
            ' \n2. Авторизация в системе'
            ' \n3. Восстановление пароля: ')
        try:
            option = int(input())
            if option in options_list:
                return option
        except ValueError:
            print('Введите номер')

def check_login(cursor):

    cursor.execute('''select Login, Password, Code from users_data;''')
    login_on_table = cursor.fetchall()
    loginID_list = []
    for i in range(len(login_on_table)):
        loginID_list.append(login_on_table[i][0])
    while True:
        print('Введите Ваш логин:')
        login = input()
        if len(login) < 2:
            print('Длина логина должна превышать 1 символ')
            print('Попробуйте снова?')
            print('Выберите Y/N')
            answer = input()
            answer = answer.lower()
            if answer == 'y':
                continue
            else:
                break
        elif login in loginID_list:
            print('Логин уже занят')
            print('Попробуйте снова?')
            print('Выберите Y/N')
            answer = input()
            answer = answer.lower()
            if answer == 'y':
                continue
            else:
                break
        elif login not in loginID_list and len(login) >= 2:
            return login
        else:
            return check_login(cursor)

def check_password():
    while True:
        print('Введите Ваш пароль:')
        password = input()
        if len(password) <= 5:
            print('Пароль должен быть длиннее 5 символов')
            print('Попробуйте снова?')
            print('Выберите Y/N')
            answer = input()
            answer = answer.lower()
            if answer == 'y':
                continue
            else:
                break
        if len(password) > 5:
            print(f'Ваш Пароль: {password}')
            return password
        else:
            return check_password()

def registration(cursor):
    """
    :return: логин, пароль, код
    """
    while True:
        login = check_login(cursor)
        if login is None:
            break
        password = check_password()
        if password is None:
            break
        if login is not None and password is not None:
            code = check_that_int()
            if code:
                return login, password, code
        print('Вы ввели неверные данные')
        break

def gen_dict(val):
    result = val
    login_password = {}
    for login, password, code in list(result):
        login_password[login] = password, code
    return login_password


def check_login_and_password(database_dict):
    while True:
        print('Введите Ваш логин: ')
        login = input()
        if login in database_dict:
            print('Логин правильный')
        else:
            print('Пользователь не зарегистрирован')
            break
        print('Введите Ваш пароль: ')
        password = input()
        if password in database_dict.get(login):
            print('Пароль правильный')
            print('Успешная авторизация')
            break
        else:
            print('Неверный пароль')
            print('Попробуйте снова?')
            print('Выберите Y/N')
            answer = input()
            answer = answer.lower()
            if answer == 'y':
                continue
            else:
                break

def recovery_password(database_dict):
    while True:
        print('Введите Ваш логин: ')
        login = input()
        if login in database_dict:
            print('Логин верный')
        else:
            while login not in database_dict:
                print('Пользователь не зарегистрирован')
                break
            break
        print('Введите код: ')
        code = input()
        if code == str(database_dict.get(login)[1]):
            print('Код верный')
            while True:
                print('Введите Ваш новый пароль:')
                password = input()
                if len(password) <= 5:
                    print('Пароль должен быть длиннее 5 символов')
                    print('Попробуйте снова?')
                    print('Выберите Y/N')
                    answer = input()
                    answer = answer.lower()
                    if answer == 'y':
                        continue
                if len(password) > 5:
                    print(f'Ваш новый пароль: {password}')
                    print('Пароль был восстановлен')
                    return password, login
                else:
                    break
            break
        else:
            print('Код неверен')
            print('Попробуйте снова?')
            print('Выберите Y/N')
            answer = input()
            answer = answer.lower()
            if answer == 'y':
                continue
            else:
                break

def connect_to_db(path_to_db):
    try:
        db = sqlite3.connect(path_to_db)
        print('Подключение к БД прошло успешно')
        return db
    except Exception as error:
        print(f"Что-то пошло не так.Ошибка: {error}")
        exit(-1)

def create_table(cursor, db):
    try:
        user_value = "('Ivan', 'qwer1234', 1234)"
        cursor.executescript(
            f'''CREATE TABLE IF NOT EXISTS users_data
            (Login text not null primary key, Password text not null , Code  integer not null);
            INSERT INTO users_data(Login, Password, Code)
            values {user_value};''')
        print('Таблица создана')
        print('Пользователь добавлен')
        db.commit()
    except Exception as error:
        print(f"При создании таблицы и добавлении пользователя произошла ошибка: {error}")

def main(path_to_db):
    db = connect_to_db(path_to_db)
    cursor = db.cursor()
    create_table(cursor, db)
    try:
        choice = select_option()
        if choice == 1:
            try:
                login, password, code = registration(cursor)
            except TypeError:
                print('Обязательные поля: Логин, Пароль, Код!!!')
            cursor.execute('''select Login, Password, Code from users_data;''')
            login_on_table = cursor.fetchall()
            loginID_list = []
            for i in range(len(login_on_table)):
                loginID_list.append(login_on_table[i][0])
            try:
                if login not in loginID_list:
                    cursor.execute(f'''INSERT INTO users_data
                                        VALUES ('{login}','{password}', {code})''')
                    db.commit()
                    print(f'Вы успешно создали пользователя:')
                    print(f'Логин {login}', f'Пароль: {password}', f'Код: {code}.', sep=', ')
                    print(f'Регистрация успешно завершена')
                else:
                    print('Логин уже занят!!!')
            except Exception as Ex:
                print('Попробуйте снова!\n')
        if choice == 2:
            print('Авторизация в системе')
            cursor.execute('''Select Login, Password, Code from users_data;''')
            result = cursor.fetchall()
            database_dict = gen_dict(result)
            check_login_and_password(database_dict)
        if choice == 3:
            cursor.execute('''Select Login, Password, Code from users_data;''')
            result = cursor.fetchall()
            database_dict = gen_dict(result)
            try:
                new_password, user_name = recovery_password(database_dict)
                cursor.execute(f"""UPDATE users_data SET Password = '{new_password}' WHERE Login = '{user_name}';""")
                db.commit()
            except Exception as Ex:
                print('Пароль не был восстановлен.\n')
    finally:
            cursor.close()

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_NAME = "registration.db"
    PATH_TO_DB = os.path.join(BASE_DIR, DB_NAME)
    main(PATH_TO_DB)

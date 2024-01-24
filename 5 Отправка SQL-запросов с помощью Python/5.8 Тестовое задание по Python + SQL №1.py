import sqlite3
from pathlib import Path

DATABASE_DIR = Path(__file__).parent


def check_that_int():
    """
    Эта функция проверяет, что пользователь вводит int
    :return: num
    """
    while True:
        print('Введите код:')
        try:
            num = int(input())
            return num
        except Exception as Ex:
            print('Введите номер!\n', Ex)


def select_one_option():
    """
    Выберите один из вариантов:
    1=Регистрация нового пользователя

    2=Авторизация в системе

    3=Восстановление пароля
    :return: option
    """

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


def check_login():
    """
    :return: логин или проверка логина
    """
    db = sqlite3.connect(DATABASE_DIR / (r'registration' + '.db'))  # Создание БД
    print('Подключились к базе данных')
    cur = db.cursor()
    cur.execute('''select Login, Password, Code from users_data;''')
    login_on_table = cur.fetchall()
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
            return check_login()


def check_password():
    """
    :return: пароль или проверка пароля
    """
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
                break


def registration():
    """
    :return: логин, пароль, код
    """
    while True:
        login = check_login()
        if login is None:
            break
        password = check_password()
        if password is None:
            break
        if login is not None and password is not None:
            try:
                code = check_that_int()
                return login, password, code
            except Exception as Ex:
                print('Вы ввели неверные данные\n', Ex)
                break
        else:
            print('Вы ввели неверные данные')
            break


def gen_dict(val):
    """
    :param val:
    :return: login_password
    """
    result = val
    login_password = {}
    for login, password, code in list(result):
        login_password[login] = password, code
    return login_password


def check_login_and_password(database_dict):
    """
    :param database_dict:
    :return:
    """
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
    """
    :param database_dict:
    :return: password, login
    """
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


'''Создание базы данных'''
try:
    db = sqlite3.connect(DATABASE_DIR / (r'registration' + '.db'))
    print('Подключились к базе данных')
    cur = db.cursor()
    '''Создание таблицы users_data'''
    user_value = "('Ivan', 'qwer1234', 1234)"
    cur.executescript(f'''CREATE TABLE IF NOT EXISTS users_data
                        (Login text not null primary key ,
                         Password text not null ,
                         Code  integer not null);

                         INSERT INTO users_data(Login, Password, Code)
                            values {user_value};''')
    db.commit()
    cur.execute('''select "Login" from users_data;''')
    user_in_db = cur.fetchall()
    print('Таблица создана')
    print('Пользователь добавлен')
except Exception as Ex:
    print(Ex)
    try:
        choice = select_one_option()
        if choice == 1:
            try:
                login, password, code = registration()
            except TypeError:
                print('Обязательные поля: Логин, Пароль, Код!!!')
            cur.execute('''select Login, Password, Code from users_data;''')
            login_on_table = cur.fetchall()
            loginID_list = []
            for i in range(len(login_on_table)):
                loginID_list.append(login_on_table[i][0])
            try:
                if login not in loginID_list:
                    cur.execute(f'''INSERT INTO users_data
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
            cur.execute('''Select Login, Password, Code from users_data;''')
            result = cur.fetchall()
            database_dict = gen_dict(result)
            check_login_and_password(database_dict)
        if choice == 3:
            cur.execute('''Select Login, Password, Code from users_data;''')
            result = cur.fetchall()
            database_dict = gen_dict(result)
            try:
                new_password, user_name = recovery_password(database_dict)
                cur.execute(f"""UPDATE users_data SET Password = '{new_password}' WHERE Login = '{user_name}';""")
                db.commit()
            except Exception as Ex:
                print('Пароль не был восстановлен.\n')

    finally:
        cur.close()

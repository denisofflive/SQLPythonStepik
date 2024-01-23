import sqlite3
from pathlib import Path

DATABASE_DIR = Path(__file__).parent

exchange_data = {1: 'RUB', 2: 'USD', 3: 'EUR'}
database_users = {1: 'Balance_RUB', 2: 'Balance_USD', 3: 'Balance_EUR'}
exchange_rates = {'USD': {'RUB': 70, 'EUR': 0.87},
                  'EUR': {'USD': 1.15, 'RUB': 80},
                  'RUB': {'USD': 0.07, 'EUR': 0.08}}

def select_currency():
    """Возвращает одно значение из заданных параметров
    :return -> int"""
    options_list = [1, 2, 3]
    while True:
        print('Введите какую валюту желаете получить: \n1. RUB \n2. USD \n3. EUR')
        try:
            option = int(input("Введите номер валюты: "))
            if option in options_list:
                return option
        except ValueError:
            print('Введите номер.')


def what_amount_are_you_interested_in():
    """
    Takes amount value and checks if it is greater than 0
    :return: option
    """
    while True:
        print('Какая сумма Вас интересует?: ')
        try:
            option = int(input())
            amount = option
            if type(option) == int:
                print(f'Вы ввели сумму: {amount}')
                if amount <= 0:
                    print('Сумма должна быть больше 0')
                    continue
                else:
                    return option
        except ValueError:
            print('Введите номер валюты.')


def select_currency_for_exchange(error):
    """
    Предлагает выбрать один из доступных вариантов, исключая переданное значение (ошибка)
    :param error:
    :return: int(option)
    """
    options_list = [1, 2, 3]
    while True:
        print('Какую валюту готовы предложить взамен?: \n1. RUB \n2. USD \n3. EUR')
        print('Помните, что вы не можете обменивать одни и те же валюты.')
        print(f'Выберите другое значение, отличное от: {error}')
        try:
            option = input()
            if int(option) in options_list and int(option) != error:
                return int(option)
        except ValueError:
            print('You must enter option number.')


def check_that_user_have_enough_money(user_money, request):
    """
    Сравниваем, что у пользователя достаточно денег:
    :param user_money:
    :param request:
    :return: request
    """
    while True:
        if user_money > request:
            return request
        else:
            while user_money < request:
                print('У вас недостаточно денег.')
                request = what_amount_are_you_interested_in()
            return request


'''Создание базы данных'''
database = sqlite3.connect(DATABASE_DIR / (r'exchanger' + '.db'))  # Creating database
print('Connecting to database...')
cursor = database.cursor()  # Variable to control the database
try:

    '''Создание таблицы users_data'''
    user_value = "(100000, 1000, 1000)"
    cursor.executescript(f'''CREATE TABLE IF NOT EXISTS users_balance(
                             LoginID INTEGER PRIMARY KEY AUTOINCREMENT,
                             Balance_RUB INTEGER not null,
                             Balance_USD INTEGER not null,
                             Balance_EUR INTEGER not null);

                             INSERT INTO users_balance(Balance_RUB, Balance_USD, Balance_EUR)
                                values {user_value};''')
    database.commit()
    cursor.execute('''select "Login" from users_balance;''')
    user_in_database = cursor.fetchall()
    print('Таблица создана.')
    print(f'Пользователь добавлен.\n')
    print('Добро пожаловать в наш обменный пункт, курс валют следующий:')
    print('1 USD = 70 RUB\n1 EUR = 80 RUB\n1 USD = 0.87 EUR\n1 EUR = 1.15 USD\n')
    selected_currency = select_currency()
    cursor.execute(f'''select {database_users.get(selected_currency)} from users_balance''')
    user_data = cursor.fetchall()
    print('На вашем балансе::', round(float(user_data[0][0]), 2), exchange_data.get(selected_currency))
    sum_for_change = what_amount_are_you_interested_in()
    selected_sum = check_that_user_have_enough_money(float(user_data[0][0]), sum_for_change)
    currency_for_exchange = select_currency_for_exchange(selected_currency)
    print()
    print('Доступные средства для обмена', user_data[0][0], exchange_data.get(selected_currency))
    print('Валюта, подлежащая обмену:', selected_sum, exchange_data.get(selected_currency))
    rate = exchange_rates.get(exchange_data.get(selected_currency)).get(exchange_data.get(currency_for_exchange))
    cash = selected_sum * rate
    print('Курс, который мы меняем', rate, exchange_data.get(currency_for_exchange))
    print(f'Вы получаете: {round(cash, 2)}', exchange_data.get(currency_for_exchange))
    minus_balance_name = database_users.get(selected_currency)
    plus_balance_name = database_users.get(currency_for_exchange)
    cursor.execute(f'''select {database_users.get(currency_for_exchange)} from users_balance''')
    plus_currency = cursor.fetchall()
    plus_currency = plus_currency[0][0]
    minus_currency = user_data[0][0]
    cursor.execute(f"""UPDATE users_balance SET {minus_balance_name} = '{minus_currency - selected_sum}';""")
    database.commit()
    cursor.execute(f"""UPDATE users_balance SET {plus_balance_name} = '{plus_currency + cash}';""")
    database.commit()
    cursor.execute(f'''select * from users_balance;''')
    current_balance = cursor.fetchall()
    print('Ваш текущий баланс:\n', round(float(current_balance[0][1]), 2), exchange_data.get(1), '\n',
          round(float(current_balance[0][2]), 2), exchange_data.get(2), '\n',
          round(float(current_balance[0][3]), 2), exchange_data.get(3))

finally:
    cursor.close()

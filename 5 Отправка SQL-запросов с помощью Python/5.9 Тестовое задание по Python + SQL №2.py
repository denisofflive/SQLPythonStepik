import sqlite3

RUB = '1'
USD = '2'
EUR = '3'

currencies_names = {RUB: "RUB", USD: "USD", EUR: "EUR"}


def create_table(db, cur):
    """Создание таблицы"""
    cur.execute("""CREATE TABLE IF NOT EXISTS users_balance(
        UserID INTEGER PRIMARY KEY AUTOINCREMENT,
        Balance_RUB INTEGER NOT NULL,
        Balance_USD INTEGER NOT NULL,
        Balance_EUR INTEGER NOT NULL);
    """)
    db.commit()


def add_users(db, cur):
    """Добавление пользователя"""
    user = ('100000', '1000', '1000')
    cur.execute("""INSERT INTO users_balance(Balance_RUB, Balance_USD, Balance_EUR)
        VALUES(?, ?, ?);
    """, user)
    db.commit()


def calculate_need_money(currency_want_change, need_money, currency_want_offer):
    # USD = 70 RUB EUR = 80 RUB USD = 0.87 EUR EUR = 1.15 USD
    if currency_want_change == RUB:
        currency = {EUR: 80, USD: 70}
        return need_money / currency[currency_want_offer]
    elif currency_want_change == USD:
        currency = {EUR: 0.87, RUB: 70}
        return need_money * currency[currency_want_offer]
    elif currency_want_change == EUR:
        currency = {USD: 1.15, RUB: 80}
        return need_money * currency[currency_want_offer]


def user_balance_money_want_change(cur, currency_want_offer):
    if currency_want_offer == RUB:
        cur.execute("""SELECT Balance_RUB FROM users_balance WHERE UserID = '1';""")
    elif currency_want_offer == USD:
        cur.execute("""SELECT Balance_USD FROM users_balance WHERE UserID = '1';""")
    elif currency_want_offer == EUR:
        cur.execute("""SELECT Balance_EUR FROM users_balance WHERE UserID = '1';""")
    balance = float(cur.fetchone()[0])
    return balance


def minus_user_money(db, cur, currency_want_change, amount):
    balance = 0
    if currency_want_change == RUB:
        cur.execute("""SELECT Balance_RUB FROM users_balance;""")
        rub_balance = float(cur.fetchone()[0]) - amount
        cur.execute(f"""UPDATE users_balance SET Balance_RUB = '{rub_balance}' WHERE UserID = '1';""")
        balance = rub_balance
    elif currency_want_change == USD:
        cur.execute("""SELECT Balance_USD FROM users_balance;""")
        usd_balance = cur.fetchone()[0] - amount
        cur.execute(f"""UPDATE users_balance SET Balance_USD = '{usd_balance}' WHERE UserID = '1';""")
        balance = usd_balance
    elif currency_want_change == EUR:
        cur.execute("""SELECT Balance_EUR FROM users_balance;""")
        eur_balance = cur.fetchone()[0] - amount
        cur.execute(f"""UPDATE users_balance SET Balance_EUR = '{eur_balance}' WHERE UserID = '1';""")
        balance = eur_balance
    db.commit()
    return balance


def plus_user_money(db, cur, currency_need_change, amount):
    balance = 0
    if currency_need_change == RUB:
        cur.execute("""SELECT Balance_RUB FROM users_balance;""")
        rub_balance = float(cur.fetchone()[0]) + amount
        cur.execute(f"""UPDATE users_balance SET Balance_RUB = '{rub_balance}' WHERE UserID = '1';""")
        balance = rub_balance
    elif currency_need_change == USD:
        cur.execute("""SELECT Balance_USD FROM users_balance;""")
        usd_balance = cur.fetchone()[0] + amount
        cur.execute(f"""UPDATE users_balance SET Balance_USD = '{usd_balance}' WHERE UserID = '1';""")
        balance = usd_balance
    elif currency_need_change == EUR:
        cur.execute("""SELECT Balance_EUR FROM users_balance;""")
        eur_balance = cur.fetchone()[0] + amount
        cur.execute(f"""UPDATE users_balance SET Balance_EUR = '{eur_balance}' WHERE UserID = '1';""")
        balance = eur_balance
    db.commit()
    return balance


def main(db, cur):
    while True:
        print('Добро пожаловать в наш обменный пункт, курс валют следующий:'
              '\n1 USD = 70 RUB'
              '\n1 EUR = 80 RUB'
              '\n1 USD = 0.87 EUR'
              '\n1 EUR = 1.15 USD\n')

        currency_want_change = input('Выберите какую валюту желаете обменять:\n1 - RUB\n2 - USD\n3 - EUR\n')
        if currency_want_change not in [RUB, USD, EUR]:
            print('Ошибка! Вы выбрали неправильное число!')
            break

        print(f'Вы выбрали - {currencies_names.get(currency_want_change)}')
        values_money_want_buy = input('Какая сумма вас интересует?\n')
        if not values_money_want_buy.isdigit() or values_money_want_buy == "0":
            print('Ошибка! Вы ввели неправильную сумму.')
            break
        values_money_want_buy = float(values_money_want_buy)

        currency_want_offer = input('Какую валюту готовы предложить взамен?\n1 - RUB\n2 - USD\n3 - EUR\n')
        if currency_want_offer not in [RUB, USD, EUR]:
            print('Ошибка! Вы выбрали неправильное число!')
            break

        if currency_want_offer == currency_want_change:
            print(f'Помните, что вы не можете обменивать одни и те же валюты.'
                  f'\nВыберите другое отличное значение от : {currency_want_offer}!')
            break
        print(f'Вы выбрали -  {currency_want_offer}')

        values_money_need = calculate_need_money(currency_want_change, values_money_want_buy, currency_want_offer)
        user_balance = user_balance_money_want_change(cur, currency_want_offer)

        if user_balance < values_money_need:
            print('На счету недостаточно средств!')
            break

        currency_want_offer_balance = minus_user_money(db, cur, currency_want_offer, values_money_need)
        currency_want_change_balance = plus_user_money(db, cur, currency_want_change, values_money_want_buy)
        print(f'Обмен валюты успешно завершен!\n'
              f'Баланс:\n'
              f'{currencies_names[currency_want_change]} - {currency_want_change_balance}\n'
              f'{currencies_names[currency_want_offer]} - {currency_want_offer_balance}')
        break


if __name__ == "__main__":
    db = sqlite3.connect('exchanger.db')
    cur = db.cursor()
    create_table(db, cur)
    add_users(db, cur)
    main(db, cur)

import sqlite3

db = sqlite3.connect('exchanger.db')
cur = db.cursor()

"""Создание таблицы"""

cur.execute("""CREATE TABLE IF NOT EXISTS users_balance(
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    Balance_RUB INTEGER NOT NULL,
    Balance_USD INTEGER NOT NULL,
    Balance_EUR INTEGER NOT NULL);
""")
db.commit()

"""Добавление пользователя"""

user = ('100000', '1000', '1000')
cur.execute("""INSERT INTO users_balance(Balance_RUB, Balance_USD, Balance_EUR)
    VALUES(?, ?, ?);
""", user)
db.commit()

rub = '1'
usd = '2'
eur = '3'

'''Приветствие'''
while True:

    print('Добро пожаловать в наш обменный пункт, курс валют следующий:'
          '\n1 USD = 70 RUB'
          '\n1 EUR = 80 RUB'
          '\n1 USD = 0.87 EUR'
          '\n1 EUR = 1.15 USD\n')

    answer = input('Выберите какую валюту желаете обменять:'
                   '\n1 - RUB'
                   '\n2 - USD'
                   '\n3 - EUR\n')
    print('Вы выбрали - ' + str(answer))

    if answer == '1' or answer == '2' or answer == '3':

        amount = input('Какая сумма вас интересует?\n')

        if len(amount) == 0 or amount == '0':
            print('Ошибка! Вы ввели неправильную сумму.')
            break
        else:

            currency = input('Какую валюту готовы предложить взамен?'
                             '\n1 - RUB'
                             '\n2 - USD'
                             '\n3 - EUR\n')
            print('Вы выбрали - ' + str(currency))
            if currency == '1' or currency == '2' or currency == '3':

                """ОШИБКА - Выбор одной валюты"""

                if (answer == '1' and currency == '1') or (answer == '2' and currency == '2') or (
                        answer == '3' and currency == '3'):
                    print('Вы выбрали неподходяющую валюту!')
                    break

                """Подсчёт количества нужной валюты"""

                # RUB
                if answer == rub:

                    request_rub = cur.execute("""SELECT Balance_RUB FROM users_balance;""")
                    date_rub = cur.fetchone()

                    if float(amount) > float(date_rub[0]):
                        print('Недостаточно средств!')
                        break

                    else:
                        """Операция по вычеслению и изменению баланса пользователя"""

                        # RUB -> USD
                        if currency == usd:

                            exch_rub = float(date_rub[0]) + float(amount)

                            # Изменяем количество средств RUB
                            update_rub = cur.execute(
                                f"""UPDATE users_balance SET Balance_RUB = '{exch_rub}' WHERE UserID = '1';""")
                            db.commit()

                            request_usd = cur.execute("""SELECT Balance_USD FROM users_balance;""")
                            date_usd = cur.fetchone()

                            amount_usd = float(amount) / float(70)
                            exch_usd = float(date_usd[0]) - float(amount_usd)

                            # Изменяем количество средств USD
                            update_usd = cur.execute(
                                f"""UPDATE users_balance SET Balance_USD = '{exch_usd}' WHERE UserID = '1';""")
                            db.commit()

                            print(f'Обмен валюты совершён! Баланс RUB - {int(exch_rub)}, баланс USD - {int(exch_usd)}')
                            break
                        # RUB -> EUR
                        elif currency == eur:

                            exch_rub = float(date_rub[0]) + float(amount)

                            # Изменяем количество средств RUB
                            update_rub = cur.execute(
                                f"""UPDATE users_balance SET Balance_RUB = '{exch_rub}' WHERE UserID = '1';""")
                            db.commit()

                            request_eur = cur.execute("""SELECT Balance_EUR FROM users_balance;""")
                            date_eur = cur.fetchone()

                            amount_eur = float(amount) / float(80)
                            exch_eur = float(date_eur[0]) - float(amount_eur)

                            # Изменяем количество средств EUR
                            update_eur = cur.execute(
                                f"""UPDATE users_balance SET Balance_EUR = '{exch_eur}' WHERE UserID = '1';""")
                            db.commit()

                            print(f'Обмен валюты совершён! Баланс RUB - {int(exch_rub)}, баланс EUR - {int(exch_eur)}')
                            break
                # USD
                if answer == usd:

                    request_usd = cur.execute("""SELECT Balance_USD FROM users_balance;""")
                    date_usd = cur.fetchone()

                    if float(amount) > float(date_usd[0]):
                        print('Недостаточно средств!')
                        break
                    else:
                        # USD -> RUB
                        if currency == rub:

                            exch_usd = float(date_usd[0]) + float(amount)

                            # Изменяем количество средств USD
                            update_usd = cur.execute(
                                f"""UPDATE users_balance SET Balance_USD = '{exch_usd}' WHERE UserID = '1';""")
                            db.commit()

                            request_rub = cur.execute("""SELECT Balance_RUB FROM users_balance;""")
                            date_rub = cur.fetchone()

                            amount_rub = float(amount) * float(70)
                            exch_rub = float(date_rub[0]) - float(amount_rub)

                            # Изменяем количество средств RUB
                            update_rub = cur.execute(
                                f"""UPDATE users_balance SET Balance_RUB = '{exch_rub}' WHERE UserID = '1';""")
                            db.commit()

                            print(f'Обмен валюты совершён! Баланс USD - {int(exch_usd)}, баланс RUB - {int(exch_rub)}')
                            break

                        # USD -> EUR
                        elif currency == eur:

                            exch_usd = float(date_usd[0]) + float(amount)

                            # Изменяем количество средств USD
                            update_usd = cur.execute(
                                f"""UPDATE users_balance SET Balance_USD = '{exch_usd}' WHERE UserID = '1';""")
                            db.commit()

                            request_eur = cur.execute("""SELECT Balance_EUR FROM users_balance;""")
                            date_eur = cur.fetchone()

                            amount_eur = float(amount) / float(0.87)
                            exch_eur = float(date_eur[0]) - float(amount_eur)

                            # Изменяем количество средств EUR
                            update_eur = cur.execute(
                                f"""UPDATE users_balance SET Balance_EUR = '{exch_eur}' WHERE UserID = '1';""")
                            db.commit()

                            print(f'Обмен валюты совершён! Баланс USD - {int(exch_usd)}, баланс EUR - {int(exch_eur)}')
                            break

                # EUR
                if answer == eur:

                    request_eur = cur.execute("""SELECT Balance_EUR FROM users_balance;""")
                    date_eur = cur.fetchone()

                    if float(amount) > float(date_eur[0]):
                        print('Недостаточно средств!')
                        break
                    else:
                        # EUR -> RUB
                        if currency == rub:

                            exch_eur = float(date_eur[0]) + float(amount)

                            # Изменяем количество средств EUR
                            update_eur = cur.execute(
                                f"""UPDATE users_balance SET Balance_EUR = '{exch_eur}' WHERE UserID = '1';""")
                            db.commit()

                            request_rub = cur.execute("""SELECT Balance_RUB FROM users_balance;""")
                            date_rub = cur.fetchone()

                            amount_rub = float(amount) * float(80)
                            exch_rub = float(date_rub[0]) - float(amount_rub)

                            # Изменяем количество средств RUB
                            update_rub = cur.execute(
                                f"""UPDATE users_balance SET Balance_RUB = '{exch_rub}' WHERE UserID = '1';""")
                            db.commit()

                            print(f'Обмен валюты совершён! Баланс EUR - {int(exch_eur)}, баланс RUB - {int(exch_rub)}')
                            break
                        # EUR -> USD
                        elif currency == usd:

                            exch_eur = float(date_eur[0]) + float(amount)

                            # Изменяем количество средств EUR
                            update_eur = cur.execute(
                                f"""UPDATE users_balance SET Balance_EUR = '{exch_eur}' WHERE UserID = '1';""")
                            db.commit()

                            request_usd = cur.execute("""SELECT Balance_USD FROM users_balance;""")
                            date_usd = cur.fetchone()

                            amount_usd = float(amount) * float(1.15)
                            exch_usd = float(date_eur[0]) - amount_usd

                            # Изменяем количество средств USD
                            update_usd = cur.execute(
                                f"""UPDATE users_balance SET Balance_USD = '{exch_usd}' WHERE UserID = '1';""")
                            db.commit()

                            print(f'Обмен валюты совершён! Баланс EUR - {int(exch_eur)}, баланс USD - {int(exch_usd)}')
                            break
            else:
                print('Ошибка! Вы выбрали неправильное число!')
                break
    else:
        print('Ошибка! Вы выбрали неправильное число!')
        break

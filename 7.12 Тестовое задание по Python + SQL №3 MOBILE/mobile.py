from mobile_query import SQL_mobile


class Mobile():

    def mobile_start(self):
        SQL_mobile.create_table()

        SQL_mobile.insert_users(('User1', 10000, 2, 'Yes'))
        SQL_mobile.insert_users(('User2', 10000, 3, 'Yes'))
        SQL_mobile.insert_users(('User3', 10000, 1, 'Yes'))

        SQL_mobile.insert_tariff(('Standard', 500))
        SQL_mobile.insert_tariff(('VIP', 1000))
        SQL_mobile.insert_tariff(('Premium', 1500))

    def tariff_withdraw(self):

            SQL_mobile.active_user()
            period = input('\nВведите количество месяцев: ')
            SQL_mobile.withdraw_money(period)



mb = Mobile()
mb.mobile_start()
mb.tariff_withdraw()

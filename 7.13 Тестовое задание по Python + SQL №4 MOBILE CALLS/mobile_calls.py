from sql_mobile_call_query import SQLMobileCallsQuery


class MobileCalls:
    def monthly_write(self):
        SQLMobileCallsQuery.create_table_mobile_users()
        SQLMobileCallsQuery.create_table_mobile_price()
        SQLMobileCallsQuery.insert_user(('User1', 500))
        SQLMobileCallsQuery.insert_price((1, 2, 3))
        SQLMobileCallsQuery.cycle()


start = MobileCalls()
start.monthly_write()
exit()

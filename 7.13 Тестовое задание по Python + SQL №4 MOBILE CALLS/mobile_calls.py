import os
from sql_mobile_call_query import SQLMobileCallsQuery


class MobileCalls:
    def monthly_write(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        mobile_calls = SQLMobileCallsQuery(BASE_DIR)
        mobile_calls.create_table_mobile_users()
        mobile_calls.create_table_mobile_price()
        mobile_calls.insert_user_data(('User1', 500))
        mobile_calls.insert_price_data((1, 2, 3))
        mobile_calls.cycle()


start = MobileCalls()
start.monthly_write()
exit()

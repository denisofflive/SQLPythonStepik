import sqlite3

"""Подключение к базе данных test_sql.db"""

db = sqlite3.connect('test_sql.db')
print("Подключились к базе данных")
cur = db.cursor()

"""Изменение данных в таблице"""
update_params = ('Sokolova', 4)
# cur.execute("""UPDATE Students1 SET Last_name = 'Orlova' WHERE StudentsID = 4 """)
cur.execute("""UPDATE Students1 SET Last_name = ? WHERE StudentsID = ?; """, update_params)
# Сохранение запроса
db.commit()
print("Изменение данных в таблице Students1")

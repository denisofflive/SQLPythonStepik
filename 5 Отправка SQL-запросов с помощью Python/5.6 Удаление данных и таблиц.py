import sqlite3

"""Подключение к базе данных test_sql.db"""

db = sqlite3.connect('test_sql.db')
print("Подключились к базе данных")
cur = db.cursor()

"""Удаление данных в таблице"""

# delete_params = '3'
# # cur.execute("""DELETE FROM Students1 WHERE StudentsID = 4""")
# cur.execute("""DELETE FROM Students1 WHERE StudentsID = ?;""", delete_params)
# # Сохранение запроса
# db.commit()
# print("Удаление данных в таблице Students1")

"""Удаление таблицы"""

cur.execute("""DROP TABLE Students2""")
db.commit()
print("Удаление таблицы Students2")

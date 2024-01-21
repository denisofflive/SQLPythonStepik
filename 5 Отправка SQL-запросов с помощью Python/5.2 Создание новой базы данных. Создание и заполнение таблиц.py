import sqlite3

"""Создание новой базы данных"""

# Создание БД test_sql.db
db = sqlite3.connect('test_sql.db')
print("Подключились к базе данных")
cur = db.cursor()

# """Создание таблицы"""
#
# cur.execute("""CREATE TABLE IF NOT EXISTS Students(
#     StudentsID INTEGER PRIMARY KEY,
#     First_name TEXT NOT NULL,
#     Last_name TEXT NOT NULL);
# """)
#
# # Сохранение результата нашего запроса
# db.commit()
# print("Создание таблицы Students")
#
# """Заполнение таблицы Students"""
#
# cur.execute("""INSERT INTO Students(First_name, Last_name)
#     VALUES('Petr', 'Petrov'); """)
# db.commit()
# print("Заполнение таблицы Students")

cur.execute("""CREATE TABLE IF NOT EXISTS Students1(
    StudentsID INTEGER PRIMARY KEY AUTOINCREMENT,
    First_name TEXT NOT NULL,
    Last_name TEXT NOT NULL);
""")
# Сохранение результата нашего запроса
db.commit()
print("Создание таблицы Students1")

cur.execute("""INSERT INTO Students1(First_name, Last_name)
    VALUES('Petr', 'Petrov'); """)
db.commit()
print("Заполнение таблицы Students1")

import sqlite3

"""Создание новой базы данных"""

# Создание БД test_sql.db
db = sqlite3.connect('test_sql.db')
print("Подключились к базе данных")
cur = db.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS Students1(
    StudentsID INTEGER PRIMARY KEY AUTOINCREMENT,
    First_name TEXT NOT NULL,
    Last_name TEXT NOT NULL);
""")
# Сохранение результата нашего запроса
db.commit()
print("Создание таблицы Students1")

# """НЕБЕЗОПАСНЫЙ СПОСОБ - Заполнения таблицы Students"""
#
# cur.execute("""INSERT INTO Students1(First_name, Last_name)
#     VALUES('Petr', 'Petrov'); """)
# db.commit()
# print("Заполнение таблицы Students1")

"""БЕЗОПАСНЫЙ СПОСОБ - Заполнения таблицы Students"""
# data_students = ('Semen', 'Semenov')
data_students = [('Alex', 'Alexandrov'), ('Olga', 'Olgina')]
# Отправка нескольких значений
cur.executemany("""INSERT INTO Students1(First_name, Last_name)
    VALUES(?, ?); """, data_students)
db.commit()
print("Добавление новых данных в таблицу")

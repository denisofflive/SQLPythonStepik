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

"""Отправка нескольких запросов"""

cur.executescript("""CREATE TABLE IF NOT EXISTS Students2(
    StudentsID INTEGER PRIMARY KEY AUTOINCREMENT,
    First_name TEXT NOT NULL,
    Last_name TEXT NOT NULL);

    INSERT INTO Students2(First_name, Last_name)
    VALUES('Petr', 'Petrov');

""")
db.commit()
print("Заполнение таблицы Students2")

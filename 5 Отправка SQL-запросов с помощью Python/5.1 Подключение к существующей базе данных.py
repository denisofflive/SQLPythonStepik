import sqlite3

"""
Подключение к существующей базе данных
"""
# Подключение к БД qa_testing.db
db = sqlite3.connect(r'C:\Users\denis\qa_testing.db')
print("Подключились к базе данных")

# Переменная для управления базой данных
cur = db.cursor()

# Запрос для получения содержимого таблицы Students
cur.execute("""SELECT * FROM Students;""")

# Результат запроса получения содержимого таблицы Students
result = cur.fetchall()
# Вывести результат
print(result)
# Вывести тип данных - это будет list (список)
print(type(result))

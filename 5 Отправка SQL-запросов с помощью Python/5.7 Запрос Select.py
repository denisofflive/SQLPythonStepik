import sqlite3

"""
Подключение к существующей базе данных
"""

db = sqlite3.connect(r'C:\Users\denis\qa_testing.db')
print("Подключились к базе данных")
cur = db.cursor()
# cur.execute("""SELECT * FROM Students;""")
cur.execute("""SELECT * FROM Students WHERE StudentID = 1;""")
# # Одно значение
# result_one = cur.fetchone()
# # Несколько значений
# result_many = cur.fetchmany(2)
# Все значения
result_all = cur.fetchall()
# print(result_all[0][1])
print(result_all)
# r = (result_one[1])
# print(result_one)
# print(result_many)

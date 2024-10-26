import sqlite3 as sq

# Создание базы данных repeat_stage с таблицей для хранения информации о пользователях и их стадиях повторения

with sq.connect('intervals.db') as con:
    cur = con.cursor()

    cur.execute("""DROP TABLE IF EXISTS intervals""")  # Удаление таблицы, если она существует

    cur.execute("""CREATE TABLE IF NOT EXISTS intervals(
        user_id INTEGER,
        set_name TEXT,
        value INTEGER
    )""")
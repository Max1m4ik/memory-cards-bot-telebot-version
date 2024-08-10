import sqlite3 as sq

with sq.connect('sets.db') as con:
    cur = con.cursor()

    cur.execute("""DROP TABLE IF EXISTS sets""") # удаление таблицы

    cur.execute("""CREATE TABLE IF NOT EXISTS cards(
        user_id INTEGER,
        set_name TEXT
    )""")
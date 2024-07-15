import sqlite3 as sq

# INSERT INTO (имя таблицы) (столбцы) VALUES (значения)  - вставка данных
# SELECT (столбцы) FROM (имя таблицы) WHERE (условие)  - выборка данных

with sq.connect('cards.db') as con:
    cur = con.cursor()

    cur.execute("""DROP TABLE IF EXISTS cards""") # удаление таблицы

    cur.execute("""CREATE TABLE IF NOT EXISTS cards(
        number INTERGER,
        question TEXT NOT NULL,
        answer TEXT NOT NULL
    )""")
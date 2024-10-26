import sqlite3 as sq

# INSERT INTO (имя таблицы) (столбцы) VALUES (значения)  - вставка данных
# SELECT (столбцы) FROM (имя таблицы) WHERE (условие)  - выборка данных

with sq.connect('user_timezones.db') as con:
    cur = con.cursor()

    cur.execute("""DROP TABLE IF EXISTS user_timezones""") # удаление таблицы

    cur.execute("""CREATE TABLE IF NOT EXISTS user_timezones(
        user_id INTEGER,
        place TEXT,
        type INTEGER
    )""")
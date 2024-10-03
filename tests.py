import sqlite3 as sq

with sq.connect('test.db') as con:
    cur = con.cursor()

    #cur.execute("""DROP TABLE IF EXISTS test""") # удаление таблицы

    cur.execute("""CREATE TABLE IF NOT EXISTS test(
        user_id INTEGER,
        set_name TEXT
    )""")
    
    cur.execute(f"""INSERT INTO test (user_id, set_name) VALUES (? , ?)""", (1, 'test'))
    
    cur = con.cursor()
    x = 1    
    cur.execute(f"SELECT set_name FROM test WHERE user_id = {x}")             
    set = cur.fetchall()
    print(set)
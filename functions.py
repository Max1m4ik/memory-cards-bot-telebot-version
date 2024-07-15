import sqlite3 as sq

def update():
    global col_of_q
    with sq.connect('cards.db') as con:
        cur = con.cursor()
        cur.execute("""SELECT question FROM cards""")
        lines = cur.fetchall()
        col_of_q = len(lines)
        for i in range (1, col_of_q):
            cur.execute(f"""UPDATE cards SET number = {i}""")

def quest(number):
    global question
    with sq.connect('cards.db') as con:
        cur = con.cursor()
        cur.execute(f"""SELECT question FROM cards WHERE number = {number}""")
        question = cur.fetchall()

def answ(number):
    global answer
    with sq.connect('cards.db') as con:
        cur = con.cursor()
        cur.execute(f"""SELECT answer FROM cards WHERE number = {number}""")
        answer = cur.fetchall()
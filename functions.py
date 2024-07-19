import sqlite3 as sq
from itertools import groupby

question = []
answer = ''
question_for_add = ''
answer_for_add = ''
col_of_q = 0

def update():
    global col_of_q
    with sq.connect('cards.db') as con:
        cur = con.cursor()
        cur.execute("""SELECT question FROM cards""")
        questions = cur.fetchall()
        unique_questions = [el for el, _ in groupby(questions)]
        col_of_q = len(unique_questions)
        for i in range (1, col_of_q + 1):
            q = (str(unique_questions[i-1])[2:-3])
            #print(q)
            cur.execute("""UPDATE cards SET number = ? WHERE question = ? """, (i, q))

def add(question, answer):
    with sq.connect('cards.db') as con:
        cur = con.cursor()
        cur.execute(f"""INSERT INTO cards (number, question, answer) VALUES (? , ? , ?)""", (col_of_q+1, question, answer))

def quest(number):
    global question
    with sq.connect('cards.db') as con:
        cur = con.cursor()
        cur.execute(f"""SELECT question FROM cards WHERE number = {number}""")
        question = cur.fetchall()
        question = str(question[0])[2:-3]
        print(question)

def answ(number):
    global r_answer
    with sq.connect('cards.db') as con:
        cur = con.cursor()
        cur.execute(f"""SELECT answer FROM cards WHERE number = {number}""")
        r_answer = cur.fetchall()
        r_answer = str(r_answer[0])[2:-3]
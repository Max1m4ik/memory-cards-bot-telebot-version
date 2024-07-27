import telebot
from telebot import types
from config import TOKEN
#from functions import *
from itertools import groupby
import sqlite3 as sq


bot=telebot.TeleBot(TOKEN)
correct = 0
stage = 'null' 
my_message = 1
user_id = 0
question_counter = 1
check_stage = 0 

def update():
    global col_of_q
    with sq.connect('cards.db') as con:
        cur = con.cursor()
        cur.execute("""SELECT question FROM cards WhERE user_id = ?""", (user_id,))
        questions = cur.fetchall()
        unique_questions = [el for el, _ in groupby(questions)]
        col_of_q = len(unique_questions)
        for i in range (1, col_of_q + 1):
            q = (str(unique_questions[i-1])[2:-3])
            #print(q)
            cur.execute("""UPDATE cards SET number = ? WHERE question = ? AND user_id = ?""", (i, q, user_id))

def add(question, answer):
    with sq.connect('cards.db') as con:
        cur = con.cursor()
        cur.execute(f"""INSERT INTO cards (user_id, number, question, answer) VALUES (? , ? , ? , ?)""", (user_id, col_of_q+1, question, answer))

def quest(number):
    try:
        global question
        with sq.connect('cards.db') as con:
            cur = con.cursor()
            cur.execute(f"""SELECT question FROM cards WHERE number = ? AND user_id = ?""", (number, user_id))
            question = cur.fetchall()
            question = str(question[0])[2:-3]
    except IndexError:
        pass
def answ(number):
    try:
        global r_answer
        with sq.connect('cards.db') as con:
            cur = con.cursor()
            cur.execute(f"""SELECT answer FROM cards WHERE number = ? AND user_id = ?""", (number, user_id))
            r_answer = cur.fetchall()
            r_answer = str(r_answer[0])[2:-3]
    except IndexError:
        pass

def start(message):
    main_kb = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Проверить знания", callback_data="check")
    btn2 = types.InlineKeyboardButton(text="Редактировать каточки", callback_data="edit")
    main_kb.add(btn1)
    main_kb.add(btn2)
    bot.send_message(message.chat.id, "Привет, {0.first_name}!".format(message.from_user), reply_markup=main_kb)


@bot.message_handler(commands=['start'])
def start(message):
    global user_id
    user_id = message.from_user.id
    update()
    if col_of_q >= 2: 
        global my_message
        user_id = message.from_user.id
        update()
        main_kb = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text="Проверить знания", callback_data="check")
        btn2 = types.InlineKeyboardButton(text="Редактировать каточки", callback_data="edit")
        main_kb.add(btn1)
        main_kb.add(btn2)
        my_message = bot.send_message(message.chat.id, "Что вы хотите сделать?", reply_markup=main_kb)
    else:
        add_kb = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text="Добавить карточки", callback_data="add")
        add_kb.add(btn1)
        bot.send_message(message.chat.id, "У вас пока меньше 2 карточек (это минимум), добавьте их в меню ниже", reply_markup=add_kb)

@bot.message_handler(content_types=['text'])
def chek_text(message):
    global stage
    global question_for_add
    global answer_for_add
    global answer
    global r_answer
    global correct
    global check_stage
    global col_of_q
    global question_counter
    #print(stage)
    if stage == 'check':
        for i in range (2):
            if check_stage == 1:
                update()
                answ(question_counter)
                print (r_answer)

                print(question_counter, "check")
                quest(question_counter)
                bot.send_message(message.chat.id, f"Карточка номер {question_counter}: {question}")
                bot.send_message(message.chat.id, "Ваш ответ: ")
                check_stage = 2
            
            elif check_stage == 2:
                update()
                answ(question_counter)
                print(r_answer)
                answer = message.text
                if answer == r_answer:
                    bot.send_message(message.chat.id,"Правильно")
                    correct += 1
                else:
                    bot.send_message(message.chat.id,"Неправильно")

                #update()
                
                if question_counter == col_of_q:
                    check_stage = 3
                else:
                    question_counter += 1
                    check_stage = 1
            
            elif check_stage == 3:
                bot.send_message(message.chat.id,f"Правильных ответов: {correct} из {col_of_q}, ({correct / col_of_q * 100}%)")
                stage = 'null'

                start(message)

            else:
                bot.send_message(message.chat.id,"Ой ой произошла ошибка начни заного /strat")
            
    elif stage == 'add1':

        question_for_add = str(message.text)
        bot.send_message(message.chat.id,"Ответ: ")
        stage = 'add2'

    elif stage == 'add2':
        answer_for_add = str(message.text)
        add(question_for_add, answer_for_add)
        bot.send_message(message.chat.id,"Карточка успешно добавлена!")
        update()
        start(message)
        stage = 'null'
    
    elif stage == 'del':
        number_question_for_del = message.text

        with sq.connect('cards.db') as con:
            cur = con.cursor()
            cur.execute(f"DELETE FROM cards WHERE number = ? AND user_id = ?", (number_question_for_del, user_id))
        stage = 'null'
        update()
        bot.send_message(message.chat.id,"Карточка успешно удалена!")
        start(message)
    
    elif stage == 'null':
        bot.send_message(message.chat.id,"Напишите /start чтобы начать")

    else:
        bot.send_message(message.chat.id,"Что-то пошло не так , попробуй перезапустить бота - /start")


@bot.callback_query_handler(func=lambda callback: callback.data)
def chek_callback_data(callback):
    global stage
    global my_message
    global question
    global correct
    global question_counter
    global r_answer
    global check_stage
    if callback.data == "check":
        bot.send_message(callback.message.chat.id,"Вы решили проверить знания")
        quest(1)
        bot.send_message(callback.message.chat.id, f"Карточка номер 1: {question}")
        bot.send_message(callback.message.chat.id, "Ваш ответ: ")
        answ(1)
        print (r_answer)
        update()
        correct = 0
        question_counter = 1
        check_stage = 2
        stage = 'check'

    elif callback.data == "edit":
        edit_menu = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text="Добавить карточки", callback_data="add")
        btn2 = types.InlineKeyboardButton(text="Удалить карточки", callback_data="delite")
        edit_menu.add(btn1)
        edit_menu.add(btn2)
        bot.edit_message_text(chat_id = callback.message.chat.id, message_id = my_message.message_id, text = "Выберите что вы будите делать: ", reply_markup=edit_menu)

    elif callback.data == "add":
        bot.send_message(callback.message.chat.id,"Вы решили добавить карточки")
        update()
        bot.send_message(callback.message.chat.id,"Вопрос:")
        stage = 'add1'
    elif callback.data == "delite":
        bot.send_message(callback.message.chat.id,"Вы решили удалить карточки")
        update()
        text = "" 
        print(col_of_q , "col_of_q")
        for i in range (1, col_of_q+1):
            quest(i)
            answ(i)
            text += f"{i} - {question} / {r_answer}\n"
        bot.send_message(callback.message.chat.id,  text)

        bot.send_message(callback.message.chat.id,"Номер карточки которую хотите удалить: ")
        stage = 'del'

try:
    bot.polling()
except KeyboardInterrupt:
    print("Exit")
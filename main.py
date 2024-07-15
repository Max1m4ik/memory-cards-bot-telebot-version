import telebot
from telebot import types
from config import TOKEN
from functions import *
import sqlite3 as sq


bot=telebot.TeleBot(TOKEN)
question_for_add = ''
answer_for_add = ''
correct = 0
stage = 'null' 
my_message = 1
update()

@bot.message_handler(commands=['start'])
def start(message):
    global my_message
    main_kb = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Проверить знания", callback_data="check")
    btn2 = types.InlineKeyboardButton(text="Редактировать каточки", callback_data="edit")
    main_kb.add(btn1)
    main_kb.add(btn2)
    my_message = bot.send_message(message.chat.id, "Привет, {0.first_name}!".format(message.from_user), reply_markup=main_kb)

@bot.message_handler(content_types=['text'])
def chek_text(message):
    global stage
    global question_for_add
    global answer_for_add
    if stage == 'chek':
        for i in range(1, col_of_q):
            quest(i)
            bot.send_message(message.chat.id, f"Карточка номер {i}: {question}")
            bot.send_message(message.chat.id,"Ваш ответ: ")
            global answer
            global correct
            correct = 0
            answer = message.text
            if answer == question:
                bot.send_message(message.chat.id,"Правильно")
                correct += 1
            else:
                bot.send_message(message.chat.id,"Не правильно")
            
        bot.send_message(message.chat.id,f"Правильных ответов: {correct} из {col_of_q}, {correct / col_of_q * 100}% ")
        stage = 'null'
    
    elif stage == 'add1':

        question_for_add = message.text
        bot.send_message(message.chat.id,"Ответ: ")
        stage = 'add2'

    elif stage == 'add2':
        answer_for_add = message.text
        with sq.connect('cards.db') as con:
            cur = con.cursor()
            cur.execute(f"INSERT INTO cards VALUES (5, {question_for_add}, {answer_for_add})")
            #cur.execute(f"INSERT INTO cards (answer) VALUES ({answer_for_add})")
        bot.send_message(message.chat.id,"Карточка успешно добавлена!")
        update()
        stage = 'null'
    
    elif stage == 'del':
        number_question_for_del = message.text

        with sq.connect('cards.db') as con:
            cur = con.cursor()
            cur.execute(f"DELETE FROM cards WHERE number = {number_question_for_del}")
        stage = 'null'
    else:
        bot.send_message(message.chat.id,"Что-то пошло не так")


@bot.callback_query_handler(func=lambda callback: callback.data)
def chek_callback_data(callback):
    global stage
    global my_message
    if callback.data == "check":
        global stage
        bot.send_message(callback.message.chat.id,"Вы решили проверить знания")
        update()
        global correct
        correct = 0
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
        for i in range (1, col_of_q):
            quest(i)
            answ(i)
            text += f"{i} - {question} - {answer}\n"
        bot.send_message(text)

        bot.send_message(callback.message.chat.id,"Номер карточки которую хотите удалить: ")
        stage = 'del'

try:
    bot.polling()
except KeyboardInterrupt:
    print("Exit")
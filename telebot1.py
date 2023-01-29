import os

import telebot
from telebot import types, util

from parse_anekdot import parse_anekdots, ANEKDOT_TYPE, STORY_TYPE

token = os.environ.get('API_TELEBOT', '')

bot = telebot.TeleBot(token)

markup = types.InlineKeyboardMarkup()
markup.row_width = 2
markup.add(types.InlineKeyboardButton("Анекдоты", callback_data=ANEKDOT_TYPE),
           types.InlineKeyboardButton("Истории", callback_data=STORY_TYPE),
           types.InlineKeyboardButton("Raise error", callback_data="error"),
           )


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Choose type:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'error':
        raise RuntimeError()
    else:
        bot.answer_callback_query(call.id, "Loading...")
        content = parse_anekdots(call.data)
        splitted_text = util.smart_split(content, chars_per_string=3000)
        for text in splitted_text:
            bot.send_message(call.from_user.id, text)
        bot.send_message(call.from_user.id, "Choose type:", reply_markup=markup)


@bot.message_handler(commands=['test'])
def send_welcome(message):
    bot.reply_to(message, "works")


bot.infinity_polling()

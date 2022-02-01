import telebot
from flask import Flask, request
import os


app = Flask(__name__)
TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def message_start(message):
    bot.send_message(message.chat.id, 'Добрый день!')

@bot.message_handler(commands=['shop'])
def message_shop(message):
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    with open('expert_center.txt') as file:
        expert_center = [item.split(',') for item in file]

        for title, link in expert_center:
            url_button = telebot.types.InlineKeyboardButton(text = title.strip(), url = link.strip())
            keyboard.add(url_button)

        bot.send_message(message.chat.id, 'Что вас интересует?', reply_markup=keyboard)

@bot.message_handler(func=lambda x: x.text.lower().startswith('Рюкзак'))
def message_text(message):
    bot.send_message(message.chat.id, 'Рюкзак')

@app.route('/' + TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "Python Telegram Bot 30-01-2022", 200



@app.route('/')
def main():
    bot.remove_webhook()
    bot.set_webhook(url='https://bot-telegram2.herokuapp.com/' + TOKEN)
    return 'Python Telegram Bot', 200

if __name__ == '__main__':
    app.run(host ='0.0.0.0', port = int(os.environ.get('PORT', 5000)))

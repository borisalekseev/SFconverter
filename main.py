from config import TOKEN
from extensions import *
import telebot

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def hello_reply(message):
    bot.send_message(message.chat.id, HELP_MESSAGE.format(message.chat.username))


@bot.message_handler(content_types=['text'])
def get_exchange_rate(message):
    try:
        values = message.text.strip().split()
        if len(values) != 3:
            raise ConvertError("Укажите ровно три параметра. Подсказка: /help")
        response = Api.get_price(*values)
    except ConvertError as ex:
        bot.reply_to(message, ex)
    except Exception as ex:
        bot.reply_to(message, ex)
    else:
        bot.reply_to(message, response)


bot.polling(none_stop=True)

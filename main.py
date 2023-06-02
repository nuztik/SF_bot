import telebot
from telebot import types

import config
from extension import *

#создание клавиатуры
conv_markup = types.ReplyKeyboardMarkup(one_time_keyboard = True)
buttons = []
for val in keys.keys():
    buttons.append(types.KeyboardButton(val.capitalize()))
conv_markup.add(*buttons)


#запуск бота
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands = ['start']) # приветствие
def start (message: telebot.types.Message):
    text = f"Добрый день, {message.chat.username}! \n Чтобы узнать, что делает бот нажми команду:/help"
    bot.reply_to(message, text)

@bot.message_handler(commands = ['help']) # показываем, что может бот
def start (message: telebot.types.Message):
    text = "Я могу показать актуальную сумму по обмену валют: \n Какую валюту можно обменять, нажми: /values \n Посчитать сумму по текущему курсу:/convert "
    bot.reply_to(message, text)

@bot.message_handler(commands = ['values']) # список валюты
def start (message: telebot.types.Message):
    text = "Доступные валюты:"
    for i in keys.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)
@bot.message_handler(commands = ['convert']) # как работает бот, что нужно зачем сделать
def conv_start (message: telebot.types.Message):
    text = "Выберете валюту, из которой будем конвертировать:"
    bot.send_message(message.chat.id, text, reply_markup = conv_markup)
    bot.register_next_step_handler(message, base_handler)
def base_handler (message: telebot.types.Message):
    base = message.text.strip()
    text = "Выберете валюту, в которой будем конвертировать:"
    bot.send_message(message.chat.id, text, reply_markup = conv_markup)
    bot.register_next_step_handler(message, quote_handler, base)
def quote_handler (message: telebot.types.Message, base):
    quote = message.text.strip()
    text = "Введите количество конвертируемой валюты"
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, amount_handler, base, quote)
def amount_handler (message: telebot.types.Message, base, quote):
    amount = message.text.strip()
    text = "Результат вычисления"
    bot.send_message(message.chat.id, text)
    try:
        new_price = Convertor.get_price(base, quote, amount)
    except APIException as e:
        bot.send_message(message.chat.id, f'Ошибка конвертации: \n{e}')
    else:
        text = f"  {amount} {base} : {new_price}"
        bot.send_message(message.chat.id, text)
@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split()
    try:
        if len(values) != 3:
            raise APIException('Неверное количество параметров!')

        answer = Convertor.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        bot.reply_to(message, answer)
bot.polling()
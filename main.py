import telebot
from extensions import CurrencyConverter, APIException
from config import keys, TOKEN


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: telebot.types.Message):
    text = ("Вас приветствует FunnyExchanger_bot!\nЧтобы узнать цену на валюту, отправьте сообщение в формате:\n<количество первой валюты> \
    <имя первой валюты, цену которой хотите узнать> \
    <имя второй валюты, которую хотите получить> \nДля просмотра доступных валют введите: /values \
    Например, если Вы хотите узнать сколько будет 2 доллара в рублях, то команда будет: 2 доллар рубль")
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def show_values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in keys.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def converter(message):
    try:
        user = message.text.split()

        if len(user) != 3:
            raise APIException("Неправильный формат запроса")

        amount, base, quote = user
        base = base.lower()
        quote = quote.lower()

        if base not in keys or quote not in keys:
            raise APIException("Неправильные имена валют")

        converted_amount = CurrencyConverter.get_price(keys[base], keys[quote], amount)
        bot.send_message(message.chat.id, f"{amount} {base.upper()} = {converted_amount} {quote.upper()}")

    except APIException as e:
        bot.send_message(message.chat.id, f"Ошибка: {e.message}")


bot.polling()

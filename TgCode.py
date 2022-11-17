import telebot
from telebot import types

bot = telebot.TeleBot("5483888032:AAFdtfhYzyH-4nmL477kbzO8MXaXIEWDrQ0")
chatid = "@workNNmsk"

user_dict = {}
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn1 = types.KeyboardButton('Уличное освещение')
    btn2 = types.KeyboardButton('Акт вандализма')
    btn3 = types.KeyboardButton('Безнадзорные животные')
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id,
                     f"Дорогой Новомосковсец!\n\nВ этом телеграм-боте у тебя есть возможность сообщить в городские службы о возникшей проблеме, будь это уличное освещение, вандализм или безнадзорные собаки.\n\nОбращаем внимание, что для отправки обращения необходимо:"
                     "\n1) Указать местоположение "
                     "\n2) Прикрепить фотографию или видео. Важно, чтобы их можно было четко просмотреть, что позволит своевременно отреагировать соответствующей службе."
                     "\n\nПросим также обратить внимание: "
                     "\n1)Указывайте точные адресные ориентиры"
                     "\n2)Бот не обрабатывает обращения без фотографии!"
                     "\n\nБлагодарим тебя, Дорогой Новомосковец, за неравнодушие!")
    bot.send_message(message.chat.id, "Выберите проблему:", reply_markup=markup)
    bot.register_next_step_handler(message, menu)
def menu(message):
    user = message.from_user.id
    user_dict[user] = []
    if message.text == "Уличное освещение":
        msg = bot.send_message(message.chat.id, "Укажите адрес/приблизительный адрес, дом/рядом стоящие дома, иные координаты (при необходимости)",reply_markup=types.ReplyKeyboardRemove(None))
        user_dict[user].append("Уличное освещение")
        bot.register_next_step_handler(msg, photo_act1)
    if message.text == "Акт вандализма":
        msg=bot.send_message(message.chat.id,
                         "Укажите адрес/приблизительный адрес, дом/рядом стоящие дома, иные координаты (при необходимости)",
                         reply_markup=types.ReplyKeyboardRemove(None))
        user_dict[user].append("Акт вандализма")
        bot.register_next_step_handler(msg, photo_act1)
    if message.text == "Безнадзорные животные":
        msg=bot.send_message(message.chat.id,
                         "Укажите адрес/приблизительный адрес, дом/рядом стоящие дома, иные координаты (при необходимости)",
                         reply_markup=types.ReplyKeyboardRemove(None))
        user_dict[user].append("Безнадзорные животные")
        bot.register_next_step_handler(msg, photo_act1)
def photo_act1(message):
        user = message.from_user.id
        address=message.text
        msg = bot.send_message(message.chat.id, "Приложите фотографию/видео\nВажно: фотография/видео должны быть четкими, распознаваемыми!")
        bot.register_next_step_handler(msg, photo_user)
        user_dict[user].append(address)

@bot.message_handler(content_types=["photo"])
def photo_user(pic):
    if pic.content_type != "photo":
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        butback = types.KeyboardButton('/start')
        markup.add(butback)
        bot.send_message(pic.chat.id, "Вы не приложили фотографию, попробуйте еще раз:", reply_markup=markup)
    else:
        user = pic.from_user.id
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        but=types.KeyboardButton('/start')
        markup.add(but)
        bot.send_photo(chat_id="-1001745849468", photo=pic.photo[-1].file_id,
                   caption=f"Фотография⬆\nОбращение от {pic.from_user.username}\n(id:{pic.from_user.id})\n\nПроблема:{user_dict[user][0]}\n\nАдрес: {user_dict[user][1]}")
        bot.send_photo(pic.chat.id, photo=pic.photo[-1].file_id, caption=f"Ваша фотография⬆\n\nПроблема:{user_dict[user][0]}\n\nАдрес: {user_dict[user][1]}\n\nБлагодарим Вас за помощь!\n\n⬇Чтобы вернуться в главное меню, нажмите кнопку ниже⬇",reply_markup=markup)


bot.polling(none_stop=True)

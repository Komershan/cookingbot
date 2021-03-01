from sys import getdefaultencoding
import config
import telebot
import demoji
from telebot import types

getdefaultencoding()
demoji.download_codes()
bot = telebot.TeleBot(config.token)

texts = ["toast.txt"]
names = ["Гренки с яйцом и молоком"]
images = ["toast.png"]
admins = set()
admins.add("Komershan")

@bot.message_handler(commands=['go', 'start'])  # Обработка команды для старта
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item2 = types.KeyboardButton("Перейти к рецептам📗")
    item1 = types.KeyboardButton('Об авторе📢')
    markup.add(item1, item2)

    bot.send_message(message.chat.id,
                     "Привет. \nЭтот бот создан в рамках практики @Komershan в написании telegramm - ботов. Тут ты можешь найти рецепты различных блюд а так же инструкции по их приготовлению. Хорошего пользования ;)".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=["text"])
def go_send_messages(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if message.text == "Перейти к рецептам📗":
        out = "Выведи номер рецепта из следующего списка:\n"
        for i in range(0, len(texts)):
            out += str(i + 1) + ". " + names[i] + "\n"
        bot.send_message(message.chat.id, out.format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)
    elif message.text.isdigit() and int(message.text) <= len(texts):
        chat_id = message.chat.id
        index = int(message.text) - 1
        bot.send_photo(chat_id, open('toast.jpg', "rb"), open(texts[index], encoding="utf-8").read())
    elif message.text == "Об авторе📢":
        bot.send_message(message.chat.id,"Меня зовут Деревягин Саша.\n" + "Учусь в СУНЦ УрФУ, увлекаюсь олимпиадным программированием и музыкой.\n" + "Имею опыт в программировании под android и создании telegram - ботов, только начал этим заниматься (на момент февраля 2021).\n" + "Собирал беспилотник, занимался риторикой и другими вещами, но это было давно. Короче, веселая жизнь)\n" + "Подпишитесь на телеграм канал, тут будет много всего интересного: t.me/defineintlonglong".format(message.from_user, bot.get_me()),parse_mode='html', reply_markup=markup)
    elif message.text[:9] == "add_admin" and str(message.from_user.username) in admins:
        admins.add(message.text[10:])
        bot.send_message(message.chat.id,"Админ успешно добавлен".format(message.from_user, bot.get_me()),parse_mode='html', reply_markup=markup)
    elif message.text[:12] == "delete_admin" and message.from_user.username in admins:
        admins.delete(message.text[13:])
        admins.add("Komershan")
        bot.send_message(message.chat.id,"Админ успешно удален".format(message.from_user, bot.get_me()),parse_mode='html', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Неправильный формат сообщения. Пожалуйста, попробуйте еще раз.".format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)

if __name__ == "__main__":
    try:
        bot.polling(none_stop=True)
    except ConnectionError as e:
        print('Ошибка соединения: ', e)
    except Exception as r:
        print("Непридвиденная ошибка: ", r)

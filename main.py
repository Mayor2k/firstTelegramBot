import telebot
#more socks proxy:
#https':'socks5://login:pass@orbtl.s5.opennetwork.cc:port
#127.0.0.1:9150

telebot.apihelper.proxy ={'https':'socks5://14611055481:U777Vluhz8@orbtl.s5.opennetwork.cc:999'}

bot = telebot.TeleBot('674637341:AAGg5XJ5LMwwLL0ft2vnRdwX4ToinWxW-6Q')
keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('Привет', 'Пока')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start', reply_markup=keyboard1)

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет, мой создатель')
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Прощай, создатель')
        bot.send_photo(message.chat.id, "https://images.unsplash.com/photo-1481819613568-3701cbc70156?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1600&q=80")
    else:
        bot.send_message(message.chat.id, "Извините, я вас не понял")


bot.polling()
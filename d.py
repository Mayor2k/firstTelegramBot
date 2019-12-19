import telebot
from telebot import types
import socket

telebot.apihelper.proxy = {'https': 'socks5h://14611055481:U777Vluhz8@orbtl.s5.opennetwork.cc:999'}

bot = telebot.TeleBot('1054005968:AAHyddoeLLrVqUkfUd1w02dUpoiVapwSasQ')

keyboard = types.ReplyKeyboardMarkup(True, True)
keyboard.row('1', '2', '3', '4', '5', '6')
connected_devices = 6

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,'К вашей системе "Умный дом" подключено '+str(connected_devices)+' устройств\n'
                                    'Выберете устройтво для управления:',reply_markup=keyboard)
@bot.message_handler(content_types=['text'])
def send_text(message):
    for x in range(1,connected_devices+1):
        if message.text.lower() == str(x):
            sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            sock.connect(('192.168.0.177',80))
            st1='r'
            byt1=st1.encode()
            sock.send(byt1)
            st='1'
            byt=st.encode()
            sock.send(byt)
            print(x)
            print(sock.recv(1024))
            sock.close()
            #bot.send_message(message.chat.id,)

if __name__ == '__main__':
    bot.polling(none_stop=True)

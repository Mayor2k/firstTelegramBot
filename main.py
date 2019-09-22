import telebot
import time_helper
import sqlite3

#more socks proxy:
#more proxy:
#https':'socks5://login:pass@orbtl.s5.opennetwork.cc:port
#127.0.0.1:9150

telebot.apihelper.proxy ={'https':'socks5://14611055481:U777Vluhz8@orbtl.s5.opennetwork.cc:999'}

bot = telebot.TeleBot('674637341:AAGg5XJ5LMwwLL0ft2vnRdwX4ToinWxW-6Q')
user_id = bot.get_me().id

keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard.row('1', '2','3')

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    delivery_days_list = time_helper.delivery_days_list(time_helper.get_current_date()[0],
                                                        time_helper.get_current_date()[1],
                                                        time_helper.get_current_date()[2])
    conn = sqlite3.connect(r"E:\Vault\Projects\telegramBot\data.sqlite")
    cursor = conn.cursor()

    for x in range(5):
        if call.data == str(x)+'day':
            date = delivery_days_list[x][0]+"."+delivery_days_list[x][2]+"."+delivery_days_list[x][3]
            try:
                cursor.execute("INSERT INTO delivery (id,delivery_method, delivery_date) VALUES (:id,'delivery', :date)", {"date":date,"id":user_id})
            except sqlite3.IntegrityError:
                cursor.execute("UPDATE delivery SET delivery_date=:date  WHERE id=:id", {"date":date,"id":user_id})
            finally:
                conn.commit()
                conn.close()

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Welcome to the our telegram bot. Here you can track your order. What do you what to do?\n'
                                      '1 - Choose date and place for your order\n'
                                      '2 - Pickup the order\n'
                                      '3 - Track the order\n', reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == '1':
        #0-day,1-weekday,2-month,3-year
        delivery_days_list = time_helper.delivery_days_list(time_helper.get_current_date()[0],
                                                            time_helper.get_current_date()[1],
                                                            time_helper.get_current_date()[2])
        keyboard1 = telebot.types.InlineKeyboardMarkup()
        for x in range(5):
            button = telebot.types.InlineKeyboardButton(
                text=delivery_days_list[x][0]+"th "+delivery_days_list[x][2]+" - "+delivery_days_list[x][1],
                callback_data=str(x)+"day")
            keyboard1.add(button)

        bot.send_message(message.chat.id, 'Choose day, when you can get the order(except days-off)',reply_markup=keyboard1)

    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Прощай, создатель')
    else:
        bot.send_message(message.chat.id, "Sorry, I don't understand you", reply_markup=keyboard)


bot.polling(none_stop=True)
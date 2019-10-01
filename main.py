import telebot
import time_helper
import sqlite3

# more socks proxy:
# more proxy:
# https':'socks5://login:pass@orbtl.s5.opennetwork.cc:port
# 127.0.0.1:9150

telebot.apihelper.proxy = {'https': 'socks5://14611055481:U777Vluhz8@orbtl.s5.opennetwork.cc:999'}

bot = telebot.TeleBot('674637341:AAGg5XJ5LMwwLL0ft2vnRdwX4ToinWxW-6Q')
user_id = bot.get_me().id

keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard.row('1', '2', '3')


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):

    for x in range(5):
        if call.data == str(x) + 'day':
            delivery_days_list = time_helper.delivery_days_list(time_helper.get_current_date()[0],
                                                                time_helper.get_current_date()[1],
                                                                time_helper.get_current_date()[2])
            conn = sqlite3.connect(r"E:\Vault\Projects\telegramBot\data.sqlite")
            cursor = conn.cursor()
            date = delivery_days_list[x][0] + "." + delivery_days_list[x][2] + "." + delivery_days_list[x][3]
            try:
                cursor.execute("INSERT INTO delivery (id, delivery_method, delivery_date) VALUES (:id,'delivery', :date)"
                               , {"date": date, "id": user_id})
            except sqlite3.IntegrityError:
                cursor.execute("UPDATE delivery SET delivery_date=:date  WHERE id=:id", {"date": date, "id": user_id})
            finally:
                conn.commit()
                conn.close()

            keyboard2 = telebot.types.InlineKeyboardMarkup()
            button1 = telebot.types.InlineKeyboardButton(text="from 8 am to 1pm", callback_data="f8t1")
            keyboard2.add(button1)
            button2 = telebot.types.InlineKeyboardButton(text="from 1 pm am to 6pm", callback_data="f1t6")
            keyboard2.add(button2)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Choose time for delivery:", reply_markup=keyboard2)

    if call.data == "f8t1" or call.data == "f1t6":
        conn = sqlite3.connect(r"E:\Vault\Projects\telegramBot\data.sqlite")
        cursor = conn.cursor()
        if call.data == "f8t1":
            cursor.execute("UPDATE delivery SET delivery_time=:date  WHERE id=:id",
                           {"date": "from 8am to 1pm", "id": user_id})
        elif call.data == "f1t6":
            cursor.execute("UPDATE delivery SET delivery_time=:date  WHERE id=:id",
                           {"date": "from 1pm to 6pm", "id": user_id})
        conn.commit()
        cursor.execute("SELECT delivery_date FROM delivery WHERE id=:id", {"id": user_id})
        date_result = cursor.fetchall()
        cursor.execute("SELECT delivery_time FROM delivery WHERE id=:id", {"id": user_id})
        time_result = cursor.fetchall()
        date_result = time_helper.garbage(str(date_result))
        time_result = time_helper.garbage(str(time_result))
        conn.close()

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Your package will come in "+date_result+" at "+time_result)
        bot.send_message(call.message.chat.id,
                         'Do you wanna do something else?\n'
                         '1 - Choose date and place for your order\n'
                         '2 - Pickup the order\n'
                         '3 - Track the order\n', reply_markup=keyboard)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,
                     'Welcome to the our telegram bot. Here you can track your order. What do you what to do?\n'
                     '1 - Choose date and place for your order\n'
                     '2 - Pickup the order\n'
                     '3 - Track the order\n', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == '1':
        # 0-day,1-weekday,2-month,3-year
        delivery_days_list = time_helper.delivery_days_list(time_helper.get_current_date()[0],
                                                            time_helper.get_current_date()[1],
                                                            time_helper.get_current_date()[2])
        keyboard1 = telebot.types.InlineKeyboardMarkup()
        for x in range(5):
            button = telebot.types.InlineKeyboardButton(
                text=delivery_days_list[x][0] + "th " + delivery_days_list[x][2] + " - " + delivery_days_list[x][1],
                callback_data=str(x) + "day")
            keyboard1.add(button)

        bot.send_message(message.chat.id, 'Choose day, when you can get the order(except days-off)',
                         reply_markup=keyboard1)

    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Прощай, создатель')
    else:
        bot.send_message(message.chat.id, "Sorry, I don't understand you", reply_markup=keyboard)


if __name__ == '__main__':
    bot.polling(none_stop=True)

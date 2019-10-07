import json
import requests
import telebot
import time_helper
import sqlite3

telebot.apihelper.proxy = {'https': 'socks5h://14611055481:U777Vluhz8@orbtl.s5.opennetwork.cc:999'}

bot = telebot.TeleBot('674637341:AAGg5XJ5LMwwLL0ft2vnRdwX4ToinWxW-6Q')
user_id = bot.get_me().id

keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard.row('1', '2', '3')


def get_current_delivery_method():
    conn = sqlite3.connect(r"E:\dev\Projects\telegramBot\data.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT delivery_method FROM delivery WHERE id=:id", {"id": user_id})
    current_method = cursor.fetchall()
    current_method = time_helper.garbage(str(current_method))
    return current_method


def build_keyboard():
    delivery_days_list = time_helper.delivery_days_list(time_helper.get_current_date()[0],
                                                        time_helper.get_current_date()[1],
                                                        time_helper.get_current_date()[2])
    keyboard1 = telebot.types.InlineKeyboardMarkup()
    for x in range(5):
        button = telebot.types.InlineKeyboardButton(
            text=delivery_days_list[x][0] + "th " + delivery_days_list[x][2] + " - " + delivery_days_list[x][1],
            callback_data=str(x) + "day")
        keyboard1.add(button)
    return keyboard1


def show_menu(call):
    bot.send_message(call,
                     'Do you wanna do something else?\n'
                     '1 - Choose date and place for your order\n'
                     '2 - Pickup the order\n'
                     '3 - Track the order\n', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):

    for x in range(5):
        if call.data == str(x) + 'day':
            delivery_days_list = time_helper.delivery_days_list(time_helper.get_current_date()[0],
                                                                time_helper.get_current_date()[1],
                                                                time_helper.get_current_date()[2])
            conn = sqlite3.connect(r"E:\dev\Projects\telegramBot\data.sqlite")
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
        conn = sqlite3.connect(r"E:\dev\Projects\telegramBot\data.sqlite")
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
        show_menu(call.message.chat.id)
    if call.data == 'change_to_pickup':
        conn = sqlite3.connect(r"E:\dev\Projects\telegramBot\data.sqlite")
        cursor = conn.cursor()
        cursor.execute("UPDATE delivery SET delivery_method='pickup'  WHERE id=:id",
                       {"id": user_id})
        conn.commit()
        conn.close()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="You're delivery method had changed to 'pickup'")
        show_menu(call.message.chat.id)

    if call.data == 'change_to_delivery':
        conn = sqlite3.connect(r"E:\dev\Projects\telegramBot\data.sqlite")
        cursor = conn.cursor()
        cursor.execute("UPDATE delivery SET delivery_method='delivery'  WHERE id=:id",
                       {"id": user_id})
        conn.commit()
        conn.close()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Choose day, when you can get the order(except days-off)',
                              reply_markup=build_keyboard())

    if call.data == 'no':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Back to te main menu")
        show_menu(call.message.chat.id)


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

        if get_current_delivery_method() == 'pickup':
            keyboard3 = telebot.types.InlineKeyboardMarkup()
            button1 = telebot.types.InlineKeyboardButton(text="Yes, change my delivery method to 'delivery'",
                                                         callback_data="change_to_delivery")
            keyboard3.add(button1)
            button2 = telebot.types.InlineKeyboardButton(text="No", callback_data="no")
            keyboard3.add(button2)
            bot.send_message(message.chat.id, "You're current delivery method is 'pickup',"
                                              " do you want to change current delivery method?", reply_markup=keyboard3)
        else:
            bot.send_message(message.chat.id, 'Choose day, when you can get the order(except days-off)',
                             reply_markup=build_keyboard())

    elif message.text.lower() == '2':
        response = requests.get(
            "https://places.cit.api.here.com/places/v1/autosuggest?at=56.114526%2C47.198588&q=почта&Accept-Language=en-US%3Ben&app_id=x2p3TDHxbG04n0y1cC9j&app_code=gRs6qSR72e0_-k_nLMgP7A")
        todos = json.loads(response.text)
        xd_list = []
        for x in range(len(todos.get('results'))):
            if todos.get('results')[x].get('category') == 'post-office':
                xd_list.append(todos.get('results')[x].get('distance'))
            else:
                xd_list.append(0)
        closest_mail = min(x for x in xd_list if x != 0)
        delivery_days_list = time_helper.delivery_days_list(time_helper.get_current_date()[0],
                                                            time_helper.get_current_date()[1],
                                                            time_helper.get_current_date()[2])
        bot.send_message(message.chat.id, "You can take your package in " +
                         todos.get('results')[xd_list.index(closest_mail)].get('title') +
                         " after "+delivery_days_list[0][0]+"th "+delivery_days_list[0][2] +
                         "("+delivery_days_list[0][1]+")")
        bot.send_location(message.chat.id, todos.get('results')[xd_list.index(closest_mail)].get('position')[0],
                          todos.get('results')[xd_list.index(closest_mail)].get('position')[1])

        if get_current_delivery_method() == 'delivery':
            keyboard3 = telebot.types.InlineKeyboardMarkup()
            button1 = telebot.types.InlineKeyboardButton(text="Yes, change my delivery method to 'pickup'",
                                                         callback_data="change_to_pickup")
            keyboard3.add(button1)
            button2 = telebot.types.InlineKeyboardButton(text="No", callback_data="no")
            keyboard3.add(button2)
            bot.send_message(message.chat.id, "You're current delivery method is 'delivery',"
                                              " do you want to change current delivery method?", reply_markup=keyboard3)
        else:
            date = delivery_days_list[0][0] + "." + delivery_days_list[0][2] + "." + delivery_days_list[0][3]
            conn = sqlite3.connect(r"E:\dev\Projects\telegramBot\data.sqlite")
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO delivery (id, delivery_method, delivery_date) VALUES (:id,'pickup', :date)"
                               , {"date": date, "id": user_id})
            except sqlite3.IntegrityError:
                cursor.execute("UPDATE delivery SET delivery_date=:date  WHERE id=:id", {"date": date, "id": user_id})
            finally:
                conn.commit()
                conn.close()

    else:
        bot.send_message(message.chat.id, "Sorry, I don't understand you", reply_markup=keyboard)


if __name__ == '__main__':
    bot.polling(none_stop=True)

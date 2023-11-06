import telebot
from telebot import types

bot = telebot.TeleBot('6108454511:AAFy5gd1pPJxc4-PL6O2RaNHqmfUNmUXrls')

catalog = [
    {'id': 1, 'name': 'Product 1', 'price': 10, 'description': 'Description 1'},
    {'id': 2, 'name': 'Product 2', 'price': 20, 'description': 'Description 2'},
    {'id': 3, 'name': 'Product 3', 'price': 30, 'description': 'Description 3'}
]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Добро пожаловать! Вот наш каталог продуктов:')
    num_of_sends = 0

    send_product(message.chat.id, 0, num_of_sends)

def send_product(chat_id, product_idx, num_of_sends):
    if product_idx < 0 or product_idx >= len(catalog):
        bot.send_message(chat_id=chat_id, text='Товар не найден')
        return

    product = catalog[product_idx]
    product_info = f"{product['name']}\n\n" \
                   f"Цена: {product['price']} руб.\n" \
                   f"Описание: {product['description']}"

    keyboard = types.InlineKeyboardMarkup()

    if product_idx == 0:
        next_button = types.InlineKeyboardButton(text='ВПЕРЕД', callback_data='next' + str(product_idx))
        keyboard.add(next_button)
    elif product_idx == len(catalog) - 1:
        prev_button = types.InlineKeyboardButton(text='НАЗАД', callback_data='prev' + str(product_idx))
        keyboard.add(prev_button)
    else:
        prev_button = types.InlineKeyboardButton(text='НАЗАД', callback_data='prev' + str(product_idx))
        next_button = types.InlineKeyboardButton(text='ВПЕРЕД', callback_data='next' + str(product_idx))
        keyboard.add(prev_button, next_button)

    if product_idx == 0 and num_of_sends == 0:
        print("перешли")
        global message_to_edit
        # global photo_to_edit
        img = open('img.png', 'rb')
        message_to_edit = bot.send_photo(chat_id, img, caption=product_info, reply_markup=keyboard)
        # message_to_edit = bot.send_message(chat_id=chat_id, text=product_info, reply_markup=keyboard)
        print(message_to_edit)
    else:
        img = open('img.png', 'rb')
        bot.edit_message_media(chat_id=chat_id, message_id=message_to_edit.message_id, media=img, reply_markup=keyboard)
        bot.edit_message_text(chat_id=chat_id, message_id=message_to_edit.message_id, text=product_info, reply_markup=keyboard)
    num_of_sends += 1

@bot.callback_query_handler(func=lambda call: call.data[0:4] == 'next')
def handle_next_button(call):
    print(call.data[4::])
    send_product(call.message.chat.id, int(call.data[4::]) + 1, 1)

@bot.callback_query_handler(func=lambda call: call.data[0:4] == 'prev')
def handle_prev_button(call):
    print(call.data)
    send_product(call.message.chat.id, int(call.data[4::]) - 1, 1)

bot.polling()

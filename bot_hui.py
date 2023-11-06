import telebot
from telebot import types
import time

TOKEN = '6108454511:AAFy5gd1pPJxc4-PL6O2RaNHqmfUNmUXrls'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Вводится первое приветственное сообщение
    bot.reply_to(message,
                 '''
                 👆КВАНТОВАЯ ПРАКТИКА «МОИ ДЕНЬГИ Х10»

Приветствую Вас! Я -Татьяна Василец, автор 5 методов практической и квантовой психологии.

Попробуйте сделать денежную практику, которую я даю в этом видео, чтобы расширить денежное мышление и увеличить свою денежную емкость!

После просмотра напишите свои впечатления текстом ниже (я обязательно прочитаю). 

Если просто хотите продолжить, нажмите кнопку ДАЛЬШЕ 👇
                 ''',
                 reply_markup=create_continue_button1())

@bot.callback_query_handler(func=lambda call: True)
def continue_button_clicked(call):
    if call.data == 'continue1':
        # Отправляется сообщение с текстом и кнопкой "СМОТРЕТЬ"
        bot.send_message(call.message.chat.id,
                         '''
                         Посмотрите следующее видео, чтобы узнать больше о моем инновационном практическом методе квантовой психологии ТЕРАПИЯ ПОЛЯ, который дает быстрые результаты! 

Сразу после просмотра этого видео я подарю Вам 🎁 - ещё одну квантовую практику по методу ТЕРАПИЯ ПОЛЯ для решения вашей актуальной задачи!
                         ''',
                         reply_markup=create_watch_button1())
        bot.answer_callback_query(call.id)

    elif call.data == 'continue2':
        # Отправляется сообщение с текстом и кнопкой "СМОТРЕТЬ"
        bot.send_message(call.message.chat.id,
                         '''
                         Благодарю за просмотр! Вот Ваш подарок 🎁 Квантовая практика для решения актуальной задачи с помощью моего метода ТЕРАПИЯ ПОЛЯ👇
                         ''',
                         reply_markup=create_gift_button())
        bot.answer_callback_query(call.id)

    elif call.data == 'watch2':
        # Отправляется сообщение с видео и кнопкой "ДАЛЬШЕ"
        bot.send_video(call.message.chat.id, open('video.mp4', 'rb'))
        bot.send_message(call.message.chat.id,
                         '''
                         Попробуйте сделать эту практику!

Подпишитесь на мои соцсети, чтобы получать другие полезные практики:

☑️Инстаграм https://instagram.com/tatyanavasilets.blog

☑️Телеграм https://t.me/inits_terapiya

☑️ВКонтакте https://vk.com/tatyanavasilets
                         ''')
        start_test(call.message.chat.id)
        bot.answer_callback_query(call.id)

    elif call.data == 'watch1':
        # Отправляется сообщение с видео и кнопкой "ДАЛЬШЕ"
        bot.send_video(call.message.chat.id, open('video.mp4', 'rb'), reply_markup=create_continue_button2())
        bot.answer_callback_query(call.id)

    elif call.data[0:3] == 'yes' or call.data[0:2] == 'no':
        # Отправляется сообщение с видео и кнопкой "ДАЛЬШЕ"
        if int(call.data[-1]) == 5:
            bot.send_message(call.message.chat.id, '''
                             Ваш результат
                             ''')
        else:
            bot.send_message(call.message.chat.id, f"Вопрос {str(call.data[-1])}", reply_markup=create_test_keyboard(int(call.data[-1]) + 1))
            bot.answer_callback_query(call.id)
    
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_message(message):
    if message.text == 'ПРОЙТИ ТЕСТ':
        # Отправляется сообщение с тестом (5 вопросов с вариантами ответов)
        bot.send_message(message.chat.id, 'Вопрос 1: ...', reply_markup=create_test_keyboard())
    else:
        bot.reply_to(message, 'Неизвестная команда.')

def create_continue_button1():
    markup = types.InlineKeyboardMarkup()
    continue_button = types.InlineKeyboardButton('ДАЛЬШЕ', callback_data='continue1')
    markup.add(continue_button)
    return markup

def create_continue_button2():
    markup = types.InlineKeyboardMarkup()
    continue_button = types.InlineKeyboardButton('ДАЛЬШЕ', callback_data='continue2')
    markup.add(continue_button)
    return markup

def create_watch_button1():
    markup = types.InlineKeyboardMarkup()
    watch_button = types.InlineKeyboardButton('СМОТРЕТЬ', callback_data='watch1')
    markup.add(watch_button)
    return markup

def create_watch_button2():
    markup = types.InlineKeyboardMarkup()
    watch_button = types.InlineKeyboardButton('СМОТРЕТЬ', callback_data='watch2')
    markup.add(watch_button)
    return markup

def create_gift_button():
    markup = types.InlineKeyboardMarkup()
    gift_button = types.InlineKeyboardButton('ЗАБРАТЬ ПОДАРОК', callback_data='watch2')
    markup.add(gift_button)
    return markup

def create_test_keyboard(num):
    markup = types.InlineKeyboardMarkup()
    yes_button = types.InlineKeyboardButton('ДА', callback_data='yes' + str(num))
    no_button = types.InlineKeyboardButton('НЕТ', callback_data='no' + str(num))
    markup.row(yes_button, no_button)
    return markup

def start_test(chat_id):
    # Отправляется новое сообщение через ровно минуту
    bot.send_message(chat_id, 'Приглашаем вас пройти тест! Нажмите кнопку "ПРОЙТИ ТЕСТ".',
                     reply_markup=create_test_keyboard(0))

bot.polling()

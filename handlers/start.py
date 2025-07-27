import os

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
from faq import RULES

from dotenv import load_dotenv

load_dotenv()

GREETINGS = """
Добро пожаловать в наш складской бот! 
Я здесь, чтобы помочь вам с вопросами о хранении, 
учете и управлении запасами. 
Если вам нужна информация о доступных товарах, правилах хранения или 
вы хотите получить помощь с заказами — просто напишите мне!"""

def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Заказы", callback_data='orders')],
        [InlineKeyboardButton("Мои вещи", callback_data='my_items')],
        [InlineKeyboardButton("FAQ", callback_data='faq')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(GREETINGS, reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    if query.data == 'orders':
        keyboard = [[InlineKeyboardButton("Назад", callback_data='back_to_main')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text="Введите список вещей, которые хотите поместить на склад", reply_markup=reply_markup)

    elif query.data == 'my_items':
        keyboard = [[InlineKeyboardButton("Назад", callback_data='back_to_main')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text="Ваши вещи на складе", reply_markup=reply_markup)

    elif query.data == 'faq':
        keyboard = [[InlineKeyboardButton("Назад", callback_data='back_to_main')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text=RULES, reply_markup=reply_markup)

    elif query.data == 'back_to_main':
        start_new_message(query)

def start_new_message(query):
    keyboard = [
        [InlineKeyboardButton("Заказы", callback_data='orders')],
        [InlineKeyboardButton("Мои вещи", callback_data='my_items')],
        [InlineKeyboardButton("FAQ", callback_data='faq')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=GREETINGS, reply_markup=reply_markup)

def main():
    updater = Updater(os.environ["BOT_TOKEN"])
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

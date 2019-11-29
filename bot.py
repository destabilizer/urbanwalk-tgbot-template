from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Bot, ReplyKeyboardMarkup, KeyboardButton
from telegram.utils.request import Request

import config

import json
import datetime

req = Request(proxy_url=config.proxy)
bot = Bot(config.token, request=req)
upd = Updater(bot=bot, use_context=True)

dp = upd.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hello! My name is {0}".format(config.name))

def photo(update, context):
    print(update.message.photo)
    request_location(context.bot, chat_id=update.effective_chat.id)

def request_location(bot, chat_id):
    location_keyboard = KeyboardButton(text="Send location", request_location=True)
    custom_keyboard = [[ location_keyboard ]]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    bot.send_message(chat_id=chat_id,
                     text="Would you mind sharing your location with me?",
                     reply_markup=reply_markup)

def location(update, context):
    print(update.message.location)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Thank you for sharing location')

dp.add_handler(CommandHandler('start', start))
dp.add_handler(MessageHandler(Filters.photo, photo))
dp.add_handler(MessageHandler(Filters.location, location))

def main():
    upd.start_polling()
    upd.idle()

if __name__ == '__main__':
    main()

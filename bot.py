from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Bot, ReplyKeyboardMarkup, KeyboardButton
from telegram.utils.request import Request

import config

import dump
import logging

req = Request(proxy_url=config.proxy)
bot = Bot(config.token, request=req)
upd = Updater(bot=bot, use_context=True)
currentFile = None
dp = upd.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hello! My name is {0}".format(config.name))

def photo(update, context):
    global currentFile
    currentFile = update.message.photo[-1].file_id
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Thanks for sharing the picture!")
    request_location(context.bot, chat_id=update.effective_chat.id)

def voice(update, context):
    file_id = update.message.voice.file_id
    newFile = bot.get_file(file_id)
    print(file_id)
    newFile.download(str(file_id) + '.ogg')
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Thanks for sharing the audio!")
    request_location(context.bot, chat_id=update.effective_chat.id)

def request_location(bot, chat_id):
    location_keyboard = KeyboardButton(text="Send location", request_location=True)
    custom_keyboard = [[ location_keyboard ]]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    bot.send_message(chat_id=chat_id,
                     text="Would you mind sharing your location with me?",
                     reply_markup=reply_markup)

def location(update, context):
    dump.data_with_location("photo", bot.get_file(currentFile), update.message.from_user.username, update.message.location)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Thank you for sharing location')

dp.add_handler(CommandHandler('start', start))
dp.add_handler(MessageHandler(Filters.photo, photo))
dp.add_handler(MessageHandler(Filters.location, location))
dp.add_handler(MessageHandler(Filters.voice, voice))

def main():
    upd.start_polling()
    #upd.idle()

if __name__ == '__main__':
    main()

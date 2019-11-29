from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Bot
from telegram.utils.request import Request

import config


req = Request(proxy_url=config.proxy)
bot = Bot(config.token, request=req)
upd = Updater(bot=bot, use_context=True)

dp = upd.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hello! My name is {0}".format(config.name))

def photo(update, context):
    file_id = update.message.photo[-1].file_id
    newFile = bot.get_file(file_id)
    print(file_id)
    newFile.download(str(file_id) + '.jpg')
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Thanks for sharing the picture!")
                             
def voice(update, context):
    file_id = update.message.voice.file_id
    newFile = bot.get_file(file_id)
    print(file_id)
    newFile.download(str(file_id) + '.ogg')
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Thanks for sharing the audio!")

    
    

start_handler = CommandHandler('start', start)
photo_handler = MessageHandler(Filters.photo, photo)
voice_handler = MessageHandler(Filters.voice, voice)

dp.add_handler(start_handler)
dp.add_handler(photo_handler)
dp.add_handler(voice_handler)

def main():
    upd.start_polling()
    upd.idle()

if __name__ == '__main__':
    main()

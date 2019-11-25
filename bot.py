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

start_handler = CommandHandler('start', start)

dp.add_handler(start_handler)

def main():
    upd.start_polling()
    upd.idle()

if __name__ == '__main__':
    main()

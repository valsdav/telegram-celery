import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                 level=logging.DEBUG)

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import BaseFilter
from telegram import MessageEntity



updater = Updater(token='730560174:AAEj4aQyCeLQK8RuS8QYqHvEdYI_0jO32t4')
dispatcher = updater.dispatcher

        
def start(bot, update):
    bot.send_message(chat_id=update.message.chat.id,
        text='''Ciao! I'm Babbage, worker bot sitting in MiB-Fisica secret lab. Send me task!!''')

start_handler = CommandHandler('start', start)
#text_handler = MessageHandler(Filters.text, echo)

dispatcher.add_handler(start_handler)
#dispatcher.add_handler(text_handler)


updater.start_polling()

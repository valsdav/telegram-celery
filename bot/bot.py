from worker import celery
import celery.states as states
from celery.task import task
import uuid

import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                 level=logging.DEBUG)

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import BaseFilter
from telegram import MessageEntity



updater = Updater(token='730560174:AAEj4aQyCeLQK8RuS8QYqHvEdYI_0jO32t4', use_context=True)
dispatcher = updater.dispatcher
j = updater.job_queue

        
def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
        text='''Ciao! I'm Babbage, worker bot sitting in MiB-Fisica secret lab. Send me task!!''')

    
def send_update(chat_id, task_id, session_id):
    def update(context):
        bot = context.bot
        job = context.job
        res = celery.AsyncResult(task_id)
        if res.state == states.PENDING:
            bot.send_message(chat_id=chat_id,text= "Waiting..")
        else:
            bot.send_message(chat_id=chat_id,
                            text= "Done (session={})! {}".format(session_id, res.result))
            job.schedule_removal()

    return update


def incoming_job_message(update, context):
    
    chat_id  = update.message.chat.id
    # Create a unique session id using the telegram message information
    session_id = hash(str(update))
    task = celery.send_task('start_job',  
            kwargs={
                    "user": update.message.chat.username,
                    "session": session_id, 
                    "conf_url":update.message.text
                    })
    context.bot.send_message(chat_id=chat_id, text="Started session: {}".format(session_id))
    j.run_repeating(send_update(chat_id, task.id, session_id), interval=5, first=2)


start_handler = CommandHandler('start', start)
incoming_job_handler = MessageHandler(Filters.text, incoming_job_message)


dispatcher.add_handler(start_handler)
dispatcher.add_handler(incoming_job_handler)

updater.start_polling()

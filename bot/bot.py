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
    message = update.message
    # Create a unique session id using the telegram message information
    session_id = "{:%y%m%d}-{}-{}-{}".format(message.date, message.chat.username,chat_id, message.message_id)
    task = celery.send_task('start_job',  
            kwargs={
                    "user":  message.chat.username,
                    "session": session_id, 
                    "conf_url": message.text
                    })
    context.bot.send_message(chat_id=chat_id, text="Started session: {}".format(session_id))
    j.run_repeating(send_update(chat_id, task.id, session_id), interval=5, first=2)


start_handler = CommandHandler('start', start)
incoming_job_handler = MessageHandler(Filters.text, incoming_job_message)


dispatcher.add_handler(start_handler)
dispatcher.add_handler(incoming_job_handler)

updater.start_polling()


## UPDATE FORMAT
# {
#     'update_id': 851612875, 
#     'message': {
    #     'message_id': 374, 
    #     'date': 1569326696, 
    #     'chat': {
    #             'id': 102616251, 
    #             'type': 'private', 
    #             'username': 'valsdav',
    #             'first_name': 'Davide',
    #             'last_name': 'Valsecchi'},
    #      'text': 'https://dvalsecc.web.cern.ch/dvalsecc/TrainingBot/conf.yaml', 
    #      'entities': [{'type': 'url', 'offset': 0, 'length': 59}],
    #      'caption_entities': [], 
    #      'photo': [], 
    #      'new_chat_members': [],
    #      'new_chat_photo': [], 
    #      'delete_chat_photo': False, 
    #      'group_chat_created': False, 
    #      'supergroup_chat_created': False, 
    #      'channel_chat_created': False, 
    #      'from': {
    #             'id': 102616251, 'first_name': 'Davide', 
    #             'is_bot': False, 'last_name': 'Valsecchi', 
    #             'username': 'valsdav', 'language_code': 'it'}
#     }
# }
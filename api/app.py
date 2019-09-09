from worker import celery
import celery.states as states
from celery.task import task

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
j = updater.job_queue

        
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
        text='''Ciao! I'm Babbage, worker bot sitting in MiB-Fisica secret lab. Send me task!!''')

    
def send_update(chat_id, task_id):
    def update(bot, context):
        res = celery.AsyncResult(task_id)
        if res.state == states.PENDING:
            bot.send_message(chat_id=chat_id,text= "Waiting..")
        else:
            bot.send_message(chat_id=chat_id,text= "Done! {}".format(res.result))
            context.schedule_removal()
    return update


def echo(bot, update):
    num = int(update.message.text)
    task = celery.send_task('tasks.add', args=[num, num], kwargs={})
    j.run_repeating(send_update(update.message.chat_id, task.id), interval=1, first=0)


start_handler = CommandHandler('start', start)
echo_handler = MessageHandler(Filters.text, echo)


dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)

updater.start_polling()

# @app.route('/add/<int:param1>/<int:param2>')
# def add(param1: int, param2: int) -> str:
#     task = celery.send_task('tasks.add', args=[param1, param2], kwargs={})
#     response = f"<a href='{url_for('check_task', task_id=task.id, external=True)}'>check status of {task.id} </a>"
#     return response


# @app.route('/check/<string:task_id>')
# def check_task(task_id: str) -> str:
#     res = celery.AsyncResult(task_id)
#     if res.state == states.PENDING:
#         return res.state
#     else:
#         return str(res.result)

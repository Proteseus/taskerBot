import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from db import Database


# logger
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# database instance
task_db = Database()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.first_name == 'Levi':
        msg = f'Good man {update.effective_user.first_name}'
    else:
        msg = f'Bugger off'

    await update.message.reply_text(msg)


async def members(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    members_ = ""
    for member in task_db.fetch_members():
        members_ += f"Name: {member[0]} - Role: {member[1]}\n"
    await update.message.reply_text(members_)


async def tasks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    tasks_ = ""
    for task in task_db.fetch_task():
        tasks_ += f"Desc: {task[1]} - Due Date: {task[2]}\n"
    await update.message.reply_text(tasks_)


async def tasks_assigned(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    tasks_ = ""
    for task in task_db.fetch_task_assigned():
        tasks_ += f"{task[1]} - {task[3]} - Due: {task[4]}\n"
    await update.message.reply_text(tasks_)


async def user_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    tasks_ = "Your assigned tasks:\n"
    for task in task_db.fetch_user_task(update.effective_user.first_name):
        tasks_ += f"\tTask: {task[3]} - Due: {task[4]}"
    await update.message.reply_text(tasks_)

app = ApplicationBuilder().token("5397641039:AAHyu2-qrogDJmG-eygCWHWBbzVW_cdxTkU").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("members", members))
app.add_handler(CommandHandler("tasks", tasks))
app.add_handler(CommandHandler("tasks_assigned", tasks_assigned))
app.add_handler(CommandHandler("user_tasks", user_tasks))

# async def runner():
#
#     await app.initialize()
#     await app.start()
#     await app.updater.start_polling()
# app.run_polling()

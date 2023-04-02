from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
from aiogram.dispatcher.filters import Text
from create_bot import dp, bot
import mongo, pytz, config, schedule, user
from datetime import datetime

@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    sms = f'👋, {message.from_user.first_name}!'
    b1 = InlineKeyboardButton('START parser tesmanian ▶', callback_data="/schedule_start")
    b2 = InlineKeyboardButton('STOP parser tesmanian 🛑', callback_data="/schedule_stop")
    b3 = InlineKeyboardButton('site tesmanian', url=user.URL)
    try:
        await bot.send_message(chat_id=message.from_user.id, text=sms,
                               reply_markup=InlineKeyboardMarkup().add(b1).add(b2).add(b3))
        await message.delete()
    except Exception as e:
        #print(e)
        await message.reply(f'спілкування з ботом через особисте повідомлення, напиши йому:\n{config.bot_tesla}')
    Kyiv_time = str(datetime.now(pytz.timezone('Europe/Kyiv')))[0:19]
    new_user = {"_id": {
        "telegram_id": message.from_user.id},
        'first_name': message.from_user.first_name,
        'last_name': message.from_user.last_name,
        'username': message.from_user.username,
        'language_code': message.from_user.language_code,
        'date': Kyiv_time}
    try:
        mongo.db.Users.insert_one(new_user)
    except Exception as e:
        #print(e)
        pass


@dp.callback_query_handler(Text(startswith="/schedule_"))
async def callback_run(callback_query: types.CallbackQuery):
    date = callback_query.data.replace('/schedule_', '')
    START, STOP = '<b>PROCESS STARTED</b>', '<b>PROCESS STOPPED</b>'
    if date == 'start':
        task = {'_id': {'title': 'tesmanain'}, 'task': True}
        try:
            mongo.db.Schedule.update_one({"_id": {"title": 'tesmanain'}}, {"$set": {'task': True}})
        except:
            mongo.db.Schedule.insert_one(task)
        await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                    message_id=callback_query.message.message_id, text=START)
        await schedule.tesla_sms(15, 'tesmanain', config.channel_id)
    elif date == 'stop':
        mongo.db.Schedule.update_one({"_id": {"title": 'tesmanain'}}, {"$set": {'task': False}})
        await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                    message_id=callback_query.message.message_id, text=STOP)




from aiogram.utils import executor
from create_bot import dp, bot
import pytz, config, user, client
from datetime import datetime
Kyiv_time = str(datetime.now(pytz.timezone('Europe/Kyiv')))[0:19]

async def on_startup(_):
    login = user.session.post(user.URL + '/account/login', cookies=user.cookies, headers=user.headers, data=user.data)
    response = 'Response [200]'
    if login.status_code != 200:
        response = login.status_code
    sms = f'Bot Tesmanian online\n{Kyiv_time} 💙💛\nlogin to site:\n{response}'
    await bot.send_message(config.channel_id, sms, disable_notification=True)
    #print(sms)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
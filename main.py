from aiogram.utils import executor
from create_bot import dp, bot
import pytz, config, client
from datetime import datetime
Kyiv_time = str(datetime.now(pytz.timezone('Europe/Kyiv')))[0:19]

async def on_startup(_):
    sms = f'Bot Tesmanian online\n{Kyiv_time} 💙💛'
    await bot.send_message(config.channel_id, sms, disable_notification=True)
    #print(sms)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
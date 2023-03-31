from create_bot import bot
import asyncio, mongo, tesla

async def tesla_sms(s, task_name, telegram_id):
    # 's' - кількість секунд між запитом на парсер
    """ на всяк випадок ми задаємо обмежену кількість запитів - 'n'
    також - нам треба прорахувати надсилання звіту один раз на хвилину,
    якщо нових статей не має на сайті, якщо це не треба просто пишемо *True* """
    n = 0
    while n < 2400:
        n += 1
        if mongo.db.Schedule.find_one({'_id': {'title': task_name}})['task'] == False:
            break
        elif mongo.db.Schedule.find_one({'_id': {'title': task_name}})['task'] == True:
            fresh = tesla.start_parcer()
            if fresh == [] and n % 4 == 0:
                # n % 4 - означає що звіт буде надсилатися раз на хвилину
                site_uk = "<a href='https://www.tesmanian.com' >сайті</a>"
                site = "<a href='https://www.tesmanian.com' >site</a>"
                sms = f"Нових публікацій на {site_uk} поки що немає.\n" \
                      f"🤷‍♂\nThere are no new posts on the {site} yet."
                await bot.send_message(telegram_id, sms, disable_notification=True)
            elif fresh != []:
                for i in fresh:
                    await bot.send_message(telegram_id, i, disable_notification=True)
            await asyncio.sleep(s)





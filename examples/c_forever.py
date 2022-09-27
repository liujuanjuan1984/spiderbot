import datetime
import time

from spiderbot import SpiderBot

bot = SpiderBot()


while True:
    try:
        bot.get_new_posturls()
        bot.get_posts()
    except KeyboardInterrupt:
        print(datetime.datetime.now(), "KeyboardInterrupt received. Exiting...")
        break

bot.quit()

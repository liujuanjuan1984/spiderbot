import time

from spiderbot import SpiderBot

bot = SpiderBot()

while True:
    bot.get_new_posturls()
    bot.get_posts()
    time.sleep(1)

bot.quit()

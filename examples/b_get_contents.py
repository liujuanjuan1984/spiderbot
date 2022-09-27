import datetime
import signal
import sys

from spiderbot import SpiderBot

bot = SpiderBot()


def sigint_handler(signal, frame):
    print(datetime.datetime.now(), "SIGINT received. Exiting...")
    bot.quit()
    print(datetime.datetime.now(), "SpiderBot quit.")
    sys.exit(0)


signal.signal(signal.SIGINT, sigint_handler)

bot.get_profiles()
bot.get_new_posturls()
bot.get_history_posturls(1, 9)
bot.get_posts()
bot.quit()

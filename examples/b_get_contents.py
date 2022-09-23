from spiderbot import SpiderBot

bot = SpiderBot()

bot.get_profiles()
bot.get_new_posturls()
bot.get_history_posturls(1, 9)
bot.get_posts()
bot.quit()

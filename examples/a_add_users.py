from spiderbot import SpiderBot

bot = SpiderBot(skip_driver=True, init=True)

urls = ["https://weibo.com/1576218000", "https://weibo.com/2588334612"]

bot.add_users(True, *urls)

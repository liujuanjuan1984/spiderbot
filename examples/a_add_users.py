from spiderbot import SpiderBot

bot = SpiderBot(skip_driver=True, init=True)

urls = ["https://example.com/123456789", "https://example.com/123456788"]

bot.add_users(True, *urls)

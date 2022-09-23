# spiderbot

爬虫机器人。

请注意，本 repo 并未提供有效的 xpaths 语法，目前配置文件中的 xpaths 仅作示例。

### 如何部署？

1、安装 spiderbot

```sh
pip install spiderbot
```

2、安装 chrome 和 chrome driver (暂未支持其它浏览器)

安装与 chrome 版本一致的 [chromedriver](https://chromedriver.chromium.org/downloads) 并把可执行文件放在系统的 PATH 目录下

3、修改配置

参考 config_private_sample.py 创建 config_private.py 文件并更新相关字段；或者，在生成 SpiderBot 实例时，传入 db_name 和 xpaths 参数。

4、如何运行？

4.1 首次初始化 bot 时，传入 `init=True` 用于生成 database，成功执行将在当前目录下 生成 spiderbot.db 文件。

```py
from spiderbot import SpiderBot

bot = SpiderBot(skip_driver=True, init=True)
```

4.2 添加 users，如果确定爬取这些用户，则传入 True，待确认就传入 None

并不需要一开始就添加很多 users，可陆续添加。

```py
from spiderbot import SpiderBot

urls = ["https://example.com/user_a_homepage", "https://example.com/user_b_homepage"]

bot = SpiderBot()
bot.add_users(working_status=True, *urls)

```

4.3 根据需要爬取内容：昵称与头像，最新内容，历史内容。

```py
from spiderbot import SpiderBot

bot = SpiderBot()
bot.get_profiles()
bot.get_new_posturls()
bot.get_history_posturls(1, 9)
bot.get_posts()
bot.quit()
```

历史内容和 profile 只需要爬取一遍，如果有遗漏，可重复爬取；

最新内容则需要持续爬取。


### 代码格式化与检查

```sh
isort .
black .
pylint spiderbot > pylint_spiderbot.log
```
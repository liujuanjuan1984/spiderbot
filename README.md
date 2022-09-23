# spiderbot

a spider bot, published as module [spiderbot](https://pypi.org/project/spiderbot/).

### How to use?

#### Install

```sh
pip install spiderbot
```

install chrome browser and [chromedriver](https://chromedriver.chromium.org/downloads), and put chromedrive binary into the PATH dir.

#### Config

Init the config_private.py, using config_private_sample.py as example, and update the value of `XPATHS` and `DB_NAME` arguments.

or,

When Generating an instance of SpiderBot, pass the value of `xpaths` and `db_name` arguments.

#### Run it

Init the database by pass the `init=True` to Generate an instance of SpiderBot. If successed, `spiderbot.db` was created.

```py
from spiderbot import SpiderBot

bot = SpiderBot(skip_driver=True, init=True)
```

Then add users to scrawler. You can add users always as needed.

```py
from spiderbot import SpiderBot

urls = ["https://example.com/user_a_homepage", "https://example.com/user_b_homepage"]

bot = SpiderBot()
bot.add_users(working_status=True, *urls)

```

At last, do the main job: 

```py
from spiderbot import SpiderBot

bot = SpiderBot()
bot.get_profiles()
bot.get_new_posturls()
bot.get_history_posturls(1, 9)
bot.get_posts()
bot.quit()
```

[more examples](./examples/)

### Code Format

```sh
isort .
black .
pylint spiderbot > pylint_spiderbot.log
```

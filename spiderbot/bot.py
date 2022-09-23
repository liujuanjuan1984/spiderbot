# -*- coding: utf-8 -*-
# pylint: disable=broad-except
"""bot.py"""
import base64
import logging
import time
from typing import Dict, Optional

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from spiderbot.config_private import DB_NAME, XPATHS
from spiderbot.models.api import DBAPI

logger = logging.getLogger(__name__)


class SpiderBot:
    """retweet bot"""

    def __init__(
        self,
        db_name: Optional[str] = None,
        xpaths: Dict[str, str] = None,
        skip_driver: bool = False,
        **kwargs,
    ):
        """kwargs for database
        echo: Optional[bool] = False,
        reset: Optional[bool] = False,
        init: Optional[bool] = False,
        """
        if skip_driver:
            self.driver = None
        else:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--ignore-certificate-errors")
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.maximize_window()
        self.xpaths = xpaths or XPATHS

        self.db = DBAPI(db_name or DB_NAME, **kwargs)  # pylint: disable=invalid-name

    def add_users(self, working_status: Optional[bool], *user_urls):
        """add users to users table"""
        failed = []
        for user_url in user_urls:
            if not self.db.add_user(user_url, working_status):
                failed.append(user_url)
        return failed

    def get_user_history_posturls(self, user_url: str, month: int = 1, sleep: int = 10):
        """get post_urls from history by month and save to table urls"""
        logger.info("get_user_history_posturls %s 月, %s", month, user_url)
        self.driver.get(user_url)
        time.sleep(sleep)
        _buttons = self.driver.find_elements(By.XPATH, self.xpaths["history"])
        for _ele in _buttons:
            if _ele.text != f"{month}月":
                continue
            try:
                _ele.click()
                time.sleep(sleep)
                for i in range(1, 10):
                    javascript = f"window.scrollBy(0,{i*500})"
                    logger.debug("%s: javascript %s", user_url, javascript)
                    self.driver.execute_script(javascript)
                    time.sleep(sleep)

                    _elements = self.driver.find_elements(By.XPATH, self.xpaths["posts"])
                    for _ele in _elements:
                        post_url = _ele.get_attribute("href")
                        logger.debug("get href url:%s", post_url)
                        if post_url.startswith(user_url):
                            self.db.add_post_url(user_url, post_url)
            except Exception as err:
                logger.warning("%s error: %s", user_url, err)

    def get_history_posturls(
        self,
        start_month: Optional[int] = None,
        end_month: Optional[int] = None,
        sleep: int = 10,
    ):
        """get posts from history and save url to the datafile"""
        start_month = start_month or 1
        end_month = end_month or 12
        for user_url in self.db.get_users_todo(True):
            for i in range(start_month, end_month + 1):
                self.get_user_history_posturls(user_url, month=i, sleep=sleep)

    def get_user_new_posturls(self, user_url: str, sleep: int = 10):
        """get new posturls of the user_url"""
        self.driver.get(user_url)
        time.sleep(sleep)
        _elements = self.driver.find_elements(By.XPATH, self.xpaths["posts"])
        for _ele in _elements:
            post_url = _ele.get_attribute("href")
            if post_url.startswith(user_url):
                self.db.add_post_url(user_url, post_url)

    def get_new_posturls(self):
        """get new posturls"""
        for user_url in self.db.get_users_todo(True):
            self.get_user_new_posturls(user_url)

    def get_post(self, post_url: str):
        """get content from one post url and save to db"""

        self.driver.get(post_url)
        wait = WebDriverWait(self.driver, 10)
        _ele = wait.until(EC.presence_of_element_located((By.XPATH, self.xpaths["screenshot"])))
        # screenshot of post
        try:
            img = base64.b64decode(_ele.screenshot_as_base64)
        except Exception as err:
            logger.warning("%s get screenshot failed: %s", post_url, err)
            img = None

        # date
        post_time = "20" + self.driver.find_element(By.XPATH, self.xpaths["date"]).text

        # text content
        try:
            text = self.driver.find_element(By.XPATH, self.xpaths["text"]).text
        except Exception as err:
            logger.warning("%s get text failed:%s", post_url, err)
            text = None

        if img or text:
            self.db.add_post(post_url, post_time, text, img)

    def get_posts(self):
        """get the content of post_urls"""
        for post_url in self.db.get_posturls_to_getcontent():
            self.get_post(post_url)

    def get_user_profile(self, user_url: str):
        """get the user profile:name and avatar"""
        self.driver.get(user_url)
        try:
            wait = WebDriverWait(self.driver, 10)
            _element = wait.until(EC.presence_of_element_located((By.XPATH, self.xpaths["avatar"])))

        except Exception as err:
            logger.warning("%s get avatar failed: %s", user_url, err)
            return
        avatar = base64.b64decode(_element.screenshot_as_base64)
        name = self.driver.find_element(By.XPATH, self.xpaths["name"]).text
        logger.info("get_user_profile: %s %s", user_url, name)
        self.db.update_user_profile(user_url, name, avatar)

    def get_profiles(self):
        """get all profiles"""
        for user_url in self.db.get_users_to_get_profiles():
            self.get_user_profile(user_url)

    def quit(self):
        """quit the driver"""
        self.driver.quit()

# -*- coding: utf-8 -*-
# pylint: disable=singleton-comparison
"""api.py"""
import logging
from typing import Optional

from spiderbot.models.base import BaseDB
from spiderbot.models.posts import Post
from spiderbot.models.posturls import PostURL
from spiderbot.models.users import User

logger = logging.getLogger(__name__)


class DBAPI(BaseDB):
    """the api of the database"""

    def add_user(self, user_url: str, working_status: Optional[bool] = None):
        """add new user to db"""
        user = self.session.query(User).filter(User.user_url == user_url).first()
        if not user:
            self.add(
                User(
                    {
                        "user_url": user_url,
                        "working_status": working_status,
                    }
                )
            )
        return True

    def get_users_todo(self, working_status: Optional[bool] = None):
        """get the users url todo"""
        users_urls = (
            self.session.query(User.user_url).filter(User.working_status == working_status).all()
        )
        for i in users_urls:
            if i:
                logger.info("get_users_todo user url: %s", i[0])
                yield i[0]

    def get_users_to_get_profiles(self):
        """get the users url todo"""
        users_urls = (
            self.session.query(User.user_url)
            .filter(User.working_status == True)
            .filter(User.name == None)
            .all()
        )
        for i in users_urls:
            if i:
                logger.info("get_users_to_get_profiles user url: %s", i[0])
                yield i[0]

    def update_user_profile(self, user_url: str, name: str, avatar: bytes):
        """update user profile"""
        self.session.query(User).filter(User.user_url == user_url).update(
            {"name": name, "avatar": avatar}
        )
        self.commit()
        logger.info("update_user_profile %s", user_url)
        return True

    def update_user_working_status(self, user_url: str, working_status: Optional[bool] = None):
        """update status of working"""
        self.session.query(User).filter(User.user_url == user_url).update(
            {"working_status": working_status}
        )
        self.commit()
        logger.info("update_user_working_status %s", user_url)
        return True

    def add_post_url(self, user_url: str, post_url: str):
        """add post url to db"""
        url = self.session.query(PostURL).filter(PostURL.post_url == post_url).first()
        if not url:
            self.add(PostURL({"user_url": user_url, "post_url": post_url}))
        logger.info("add_post_url %s", post_url)
        return True

    def update_url_content_status(self, post_url: str, content_status: bool):
        """update post_url content status"""
        self.session.query(PostURL).filter(PostURL.post_url == post_url).update(
            {"content_status": content_status}
        )
        self.commit()
        logger.info("update_url_content_status %s", post_url)
        return True

    def get_posturls_to_getcontent(self):
        """get the urls which to get content"""

        urls = self.session.query(PostURL.post_url).filter(PostURL.content_status == None).all()
        for i in urls:
            if i:
                logger.info("get_posturls_to_getcontent %s", i[0])
                yield i[0]

    def add_post(self, post_url: str, post_time: str, text: str, screenshot: bytes):
        """add new post"""
        post = self.session.query(Post).filter(Post.post_url == post_url).first()
        if not post:
            self.add(
                Post(
                    {
                        "post_url": post_url,
                        "text": text,
                        "screenshot": screenshot,
                        "post_time": post_time,
                    }
                )
            )
        logger.info("add_post %s %s", post_url, post_time)
        self.update_url_content_status(post_url, True)
        return True

    def get_post(self, post_url: str):
        """get the post by post_url"""
        post = self.session.query(Post).filter(Post.post_url == post_url).first()
        logger.info("get_post %s", post_url)
        return post

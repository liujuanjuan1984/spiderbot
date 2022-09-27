# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods

"""users.py"""
import logging

from sqlalchemy import Boolean, Column, Integer, LargeBinary, String

from spiderbot.models.base import Base, current_time

logger = logging.getLogger(__name__)


class User(Base):
    """the target users to retweet
    working_status:
    None: new user to check
    True: user is valid to spider
    False: user is invalid to spider, such as the user is not exist or banned or usless
    """

    __tablename__ = "users"

    uid = Column(Integer, primary_key=True, unique=True, index=True)
    user_url = Column(String, unique=True, index=True)
    name = Column(String, default=None)
    working_status = Column(Boolean, default=None)
    avatar = Column(LargeBinary, default=None)
    created_at = Column(String, default=current_time)
    updated_at = Column(String, default=current_time)

    def __init__(self, obj):
        super().__init__(**obj)

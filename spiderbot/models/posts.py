# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods
"""posts.py"""
import logging

from sqlalchemy import Column, Integer, LargeBinary, String

from spiderbot.models.base import Base, current_time

logger = logging.getLogger(__name__)


class Post(Base):
    """the content of posts"""

    __tablename__ = "posts"

    uid = Column(Integer, primary_key=True, unique=True, index=True)
    post_url = Column(String, unique=True, index=True)
    text = Column(String)
    post_time = Column(String)
    screenshot = Column(LargeBinary)
    created_at = Column(String, default=current_time)
    updated_at = Column(String, default=current_time)

    def __init__(self, obj):
        super().__init__(**obj)

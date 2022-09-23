# -*- coding: utf-8 -*-
"""base.py"""
import datetime
import logging
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


def current_time():
    """get the current time and return string"""
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return now_str


logger = logging.getLogger(__name__)


class BaseDB:
    """BaseDB"""

    def __init__(
        self,
        db_name: str,
        echo: Optional[bool] = False,
        reset: Optional[bool] = False,
        init: Optional[bool] = False,
    ):
        """init the db"""
        engine = create_engine(db_name, echo=echo, connect_args={"check_same_thread": False})
        if reset:
            Base.metadata.drop_all(engine)
        if init:
            Base.metadata.create_all(engine)
        self.maker = sessionmaker(bind=engine, autoflush=False)
        self.session = self.maker()

    def __commit(self, session=None):
        """Commits the current db.session, does rollback on failure."""
        session = session or self.session

        try:
            session.commit()
        except IntegrityError:
            session.rollback()

    def add(self, obj, session=None):
        """Adds this model to the db (through db.session)"""
        session = session or self.session
        session.add(obj)
        self.__commit(session)

    def commit(self):
        """commit"""
        self.__commit()

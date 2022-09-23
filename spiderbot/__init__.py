# -*- coding: utf-8 -*-
"""spiderbot"""
import datetime
import logging

from spiderbot.bot import SpiderBot

__version__ = "0.2.0"
__author__ = "liujuanjuan1984"

# Set default logging handler to avoid "No handler found" warnings.
logging.getLogger(__name__).addHandler(logging.NullHandler())
logging.basicConfig(
    format="%(name)s %(asctime)s %(levelname)s %(message)s",
    filename=f"spiderbot_{datetime.date.today()}.log",
    level=logging.INFO,
)

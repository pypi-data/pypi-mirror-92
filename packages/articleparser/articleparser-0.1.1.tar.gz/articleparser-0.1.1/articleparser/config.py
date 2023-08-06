"""Defines a configuration object, containing mutable parameters.

Written January 2021.
"""

import logging

from articleparser.settings import (
    DECOMPOSE_TAGS,
    MARKUP_TAGS,
)

LOGGER = logging.getLogger(__name__)


class Config(object):
    def __init__(self):
        self.DECOMPOSE_TAGS = DECOMPOSE_TAGS
        self.MARKUP_TAGS = MARKUP_TAGS

        self.decompose = True
        self.cssvis = True
        self.replace_breaks = True
        self.unwrap_markup = True
        self.get_linkdensity = True

        self.LINKDENSITY_UPPERBOUND = 0.75
        self.MAX_LEVELS = 5
        self.MIN_TAGS_TO_CHECK = 1
        self.BASE_TAG_CHARS_RATIO = 0.4
        self.ARTICLE_TEXT_CHARS_RATIO = 0.1

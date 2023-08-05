# pylint: disable=missing-docstring
# -*- coding: utf-8 -*-
"""It really seems a docstring is needed here!"""

import logging
from ftrotta.pycolib.log import get_configured_root_logger


_logger = get_configured_root_logger(logging.INFO)


def test():
    _logger.debug("Debug message")
    _logger.info("Info message")

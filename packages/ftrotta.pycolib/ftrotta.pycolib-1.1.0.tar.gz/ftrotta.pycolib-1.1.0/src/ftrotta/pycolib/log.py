# -*- coding: utf-8 -*-
"""Logging facilities.

The name prevents conflicts with default logging package.
"""

import logging


def get_configured_root_logger(level: int = logging.DEBUG) -> logging.Logger:
    """Get the root logger with configured handler and formatter.

    It can be used in any top level module, to handle logging on stderr. The
    stream handler on stderr is added only in case the root logger has no
    other handlers. This prevents logging message repetitions when used in
    test modules.

    Example:
        >>> from ftrotta.pycolib.log import get_configured_root_logger
        >>>
        >>> _logger = get_configured_root_logger()
        >>>
        >>> _logger.debug('Debug message')

    Args:
        level: The logging level (set to the handler). Defaults to
            `logging.DEBUG`.

    Returns:
        The root logger, with configured handler on stderr and formatter.
    """
    logger = logging.getLogger()
    logger.setLevel(level)
    if not logger.handlers:  # pragma: no cover
        handler = logging.StreamHandler()
        format_str = '%(asctime)15s : PID:%(process)d : %(module)s.%(' \
                     'funcName)s : %(levelname)s : %(message)s'
        formatter = logging.Formatter(format_str)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

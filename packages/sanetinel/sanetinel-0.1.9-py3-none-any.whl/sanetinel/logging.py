# (c) 2020 Simon Rovder and others.
# This file is subject to the terms provided in 'LICENSE'.
import logging

_context = 'default'


class SanetinelContextFilter(logging.Filter):

    def filter(self, record):
        record.sanetinel_context = _context
        return True


def default_logging_config():
    _logger: logging.Logger = logging.getLogger('sanetinel')
    _h = logging.StreamHandler()
    _h.addFilter(SanetinelContextFilter())
    _h.setFormatter(logging.Formatter(fmt="[ %(levelname)8s - %(name)s ] (%(sanetinel_context)s) %(message)s"))
    _logger.addHandler(_h)
    _logger.propagate = False


def set_context(context: str):
    global _context
    _context = context


def get_context() -> str:
    return _context

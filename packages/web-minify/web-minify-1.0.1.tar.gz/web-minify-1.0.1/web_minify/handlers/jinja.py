import sys
import logging
from jinja2 import Environment

logger = logging.getLogger(__name__)

jinja_env = Environment()


def jinja_minify(jinja, settings: dict):
    """Minify jinja main function. Does not minify, rather detects errors (lint)
    """
    try:
        jinja_env.parse(jinja)
    except Exception as e:
        logger.error("Jinja validator: {e}")
    return jinja.strip()

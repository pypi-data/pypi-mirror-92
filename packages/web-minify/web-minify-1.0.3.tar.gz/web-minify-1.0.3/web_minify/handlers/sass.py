from .css import css_minify

import logging

logger = logging.getLogger(__name__)

have_sass = False

try:
    import sass

    have_sass = True
except Exception:
    logger.warning("Could not import sass", exc_info=True)
    logger.warning("NOTE: To install sass, please remember to use  use pip install libsass instead of pip install sass")


def sass_minify(scss, settings: dict):
    """Minify SASS main function."""
    if have_sass:
        try:
            css = sass.compile(string=scss)
        except sass.CompileError as ce:
            return (None, [f"SASS {ce}"])
        except Exception as e:
            return (None, [f"Error: Could not process SASS {e}"])
    css, css_errors = css_minify(css=css, settings=settings)
    return css, css_errors

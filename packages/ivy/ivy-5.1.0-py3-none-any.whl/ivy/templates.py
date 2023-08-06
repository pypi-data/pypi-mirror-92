# ------------------------------------------------------------------------------
# This module handles template-engine callbacks.
# ------------------------------------------------------------------------------

import sys
import pathlib
from pathlib import Path

from . import site
from . import utils
from . import pages


# Stores registered template-engine callbacks indexed by file extension.
_callbacks = {}


# Caches a list of the theme's template files.
_cache = None


# Decorator function for registering template-engine callbacks. A template-
# engine callback should accept a Page instance and a template filename and
# return a string of html.
#
# Callbacks are registered per file extension, e.g.
#
#   @ivy.templates.register('ibis')
#   def callback(page, filename):
#       ...
#       return html
#
def register(ext):

    def register_callback(callback):
        _callbacks[ext] = callback
        return callback

    return register_callback


# Render a Page instance into html.
def render(page):

    # Cache a list of the theme's template files for future calls.
    global _cache
    if _cache is None:
        root = site.theme('templates')
        _cache = [p for p in Path(root).iterdir() if p.is_file()]

    # Find the first template file matching the page's template list.
    for name in page['templates']:
        for path in _cache:
            if name == path.stem:
                ext = path.suffix.strip('.')
                if ext in _callbacks:
                    try:
                        return _callbacks[ext](page, path.name)
                    except Exception as err:
                        msg = "Template Error\n"
                        msg += f">> Template: {path.name}\n"
                        msg += f">> Node: {page['node'].url}\n"
                        msg += f">> {err.__class__.__name__}: {err}"
                        if (cause := err.__cause__):
                            msg += f"\n>> Cause: {cause.__class__.__name__}: {cause}"
                        elif (context := err.__context__):
                            msg += f"\n>> Context: {context.__class__.__name__}: {context}"
                        sys.exit(msg)
                else:
                    msg = f"Error: The template file '{path.name}' has an unrecognised extension."
                    sys.exit(msg)

    sys.exit(f"Error: Ivy cannot locate a template file for the node: '{page['node'].url}'.")

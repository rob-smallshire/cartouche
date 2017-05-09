from .parser import (rewrite_autodoc, builder_inited)
from .version import (__version__)

__author__ = 'Robert Smallshire'

def setup(app):
    if not hasattr(app, 'add_config_value'):
        return # probably called by nose, better bail out
    app.add_config_value('cartouche_accept_bulleted_args', False, 'env')
    app.add_config_value('cartouche_accept_bulleted_raises', False, 'env')
    app.connect('builder-inited', builder_inited)
    app.connect('autodoc-process-docstring', rewrite_autodoc)

    return dict(
        version = __version__,
        parallel_read_safe = True,
        parallel_write_safe = True
    )

from .parser import rewrite_autodoc

__author__ = 'Robert Smallshire'

def setup(app):
    app.connect('autodoc-process-docstring', rewrite_autodoc)

cartouche
=========

A Sphinx extension to convert help() friendly docstrings to Sphinx markup.

Welcome to `cartouche`
----------------------

`cartouche` allows you to write human readable doc-strings for use with
`help()` which can also produce beautiful Sphinx output.

Why it's needed
---------------

Sphinx is a popular tool for documenting Python APIs which uses
reStructuredText as a its lightweight markup language. Sphinx extends
restructured text with semantic markup elements for documenting Python APIs
but when these are used the ratio of markup to content becomes too high and
readability is compromised enough that the docstring becomes unsuitable for
use with standard Python introspection mechanisms like help() or IDEs.

What it does
------------

Cartouche is a Sphinx extension which automatically converts a highly readable
docstring format suitable for use with help() and IDEs to the reStructuredText
hieroglyphics required by Sphinx.

Cartouche will turn this:

```
def select(self, selector):
    '''Transforms each element of a sequence into a new form.

    Each element of the source is transformed through a selector function
    to produce a corresponding element in teh result sequence.

    If the selector is identity the method will return self.

    Note: This method uses deferred execution.

    Args:
        selector: A unary function mapping a value in the source sequence
            to the corresponding value in the generated generated sequence.
            The single positional argument to the selector function is the
            element value.  The return value of the selector function
            should be the corresponding element of the result sequence.

    Returns:
        A Queryable over generated sequence whose elements are the result
        of invoking the selector function on each element of the source
        sequence.

    Raises:
        ValueError: If this Queryable has been closed.
        TypeError: If selector is not callable.
    '''
```

into this,

![Image of cartouche rendered HTML](http://cartouche.readthedocs.org/en/latest/_images/select_html.png)

How to get it
-------------

Use ``easy_install`` or ``pip`` to fetch it from the Python Package Index

```
 > easy_install cartouche
```

or

```
 > pip install cartouche 
```

Alternatively, download the source distribution, unzip it and run ``setup.py``:

```
 > cd cartouche-0.9
 > python setup.py install
```

How to use it
-------------

Refer to the `cartouche` Sphinx extension in the `conf.py` file for your
Sphinx documentation source like this:

```
# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.

extensions = ['sphinx.ext.autodoc', 'cartouche']
````

then start writing docstrings in the form above.

Full documentation can be found here: http://cartouche.readthedocs.org/en/latest/

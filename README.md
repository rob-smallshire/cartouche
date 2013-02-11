cartouche
=========

A Sphinx extension to convert help() friendly docstrings to Sphinx markup.

Welcome to `cartouche`
----------------------

`cartouche` allows you to write human readable doc-strings for use with `help()` which can also produce beautiful Sphinx output.

Why it's needed
---------------

Sphinx is a popular tool for documenting Python APIs which uses reStructuredText as a its lightweight markup language. Sphinx extends restructured text with semantic markup elements for documenting Python APIs but when these are used the ratio of markup to content becomes too high and readability is compromised enough that the docstring becomes unsuitable for use with standard Python introspection mechanisms like help() or IDEs.

What it does
------------

Cartouche is a Sphinx extension which automatically converts a highly readable docstring format suitable for use with help() and IDEs to the reStructuredText hieroglyphics required by Sphinx.

Cartouche will turn this:

```
        Determine if all elements in the source sequence satisfy a condition.

        All of the source sequence will be consumed.

        Note: This method uses immediate execution.

        Args:
            predicate (callable) : An optional single argument function used to test each
                elements. If omitted, the bool() function is used resulting in
                the elements being tested directly.

        Returns:
            True if all elements in the sequence meet the predicate condition,
            otherwise False.

        Raises:
            ValueError: If the Queryable is closed()
            TypeError: If predicate is not callable.
```

into this,

![Image of cartouche rendered HTML](http://wiki.cartouche.googlecode.com/hg/images/sample_html.png)

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

Refer to the `cartouche` Sphinx extension in the `conf.py` file for your Sphinx documentation source like this:

```
# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.

extensions = ['sphinx.ext.autodoc', 'cartouche']
````

then start writing docstrings in the form above.

Full documentation can be found here: http://cartouche.readthedocs.org/en/latest/

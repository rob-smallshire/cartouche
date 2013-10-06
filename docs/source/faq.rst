Frequently Asked Questions
==========================

Where does the name ``cartouche`` come from?
--------------------------------------------

A **cartouche** is a symbol used in Egyptian hieroglyphs to indicate that the
enclosed text is a royal name [*]_. Since ``cartouche`` is a plugin to the
`Sphinx <http://sphinx.pocoo.org/>`_ Python documentation generator, a name
with a suitably Egyptian theme was selected. The connection to hieroglyphs is
significant, because regular Sphinx docstrings can be dense with symbols,
making them hard to read in plain text. Ironic, since the motivation behind
`reStructuredText <http://docutils.sourceforge.net/rst.html>`_ was that is
should be an "easy-to-read, what-you-see-is-what-you-get plaintext markup
syntax".

Didn't this project used to be called ``hieroglyph``?
-----------------------------------------------------

Yes. Unfortunately, somebody too lazy to do a quick Google search for "Sphinx
extension hieroglyph" beat me to an upload to the Python Package Index,
thereby securing the name for their own project. C'est la vie. Que sera sera.

Are attribute lists in class docstrings supported?
--------------------------------------------------

Not yet, although any information you place in class docstrings will pass
through ``cartouche`` unaltered.

.. [*] See the `Wikipedia article on cartouches <http://en.wikipedia.org/wiki/Cartouche>`_ for more details.
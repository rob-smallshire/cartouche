"""
An example module to be documented with Sphinx and Cartouche.

This is the example docstring for the example.py module.
"""

class Example(object):
    """The example docstring for the Example class.

    Within this class docstring we can both describe the class, but also use
    an attributes heading to list the attributes we expect the instances of
    the class to have.  There is no specific provision for distinguishing
    between class attributes and instance attributes at this point, so you
    should make that distinction clear in your descriptions.

    Attributes:
        fred: This attribute description just runs to a single line.
        shiela: This attribute description is somewhat longer and spans
             multiple lines. Subsequent lines are indented one further level.
        jim (int): As with function or method docstrings you can optionally
            provide a type in parentheses after the attribute name and before
            the colon which separates the name from the description.

        harry: With longer attribute descriptions it can help to separate the
            attributes with blank lines.  This takes up more room in the
            source code but is much easier to read when using the help()
            function.
    """

    def do_something(self, tom, dick, harry, george, *args, **kwargs):
        """Initialise an Example.

        A method docstring can contain an Args, Returns or Raises section.
        It's typically formatted like this with a brief one line description
        following by an optional separate paragraph (this one) with a longer
        description.

        Args:
            tom: This argument description just runs to a single line.
            dick: This argument description is somewhat longer and spans
                multiple lines. Subsequent lines are indented one further
                level.
            harry (int): You may optionally provide a type in parentheses
                after the attribute name and before the colon which separates
                the name from the description.

            george: With longer argument descriptions it can help to separate
                the arguments with blank likes to aid readability. This takes
                up more room in the source code but is much easier to read
                when using the help() function.

            *args: The positional arguments should be indicated with a leading
                asterisk.

            **kwargs: The keyword arguments should be indicated with two
                leading asterisks.

        Returns: A list of integers. If this desciption needs to be longer
            wrap onto the next line and indent further as necessary.

        Raises:
            ValueError: Each entry in this block should begin with an
                exception name.
            TypeError: As with argument lists these can be on adjacent lines
                like the first two.

            IndexError: Or separated by whitespace if that aids readability.
        """
        pass


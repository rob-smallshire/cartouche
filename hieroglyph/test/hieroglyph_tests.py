import unittest

from hieroglyph.hieroglyph import parse_readabletext

class CommentTests(unittest.TestCase):

    def test_comment1(self):
        source = """Fetches rows from a Bigtable.
        This is a continuation of the opening paragraph.

        Retrieves rows pertaining to the given keys from the Table instance
        represented by big_table.  Silly things may happen if
        other_silly_variable is not None.

        Args:
            big_table: An open Bigtable Table instance.
            keys: A sequence of strings representing the key of each table row
                to fetch.
            other_silly_variable (str): Another optional variable, that has a much
                longer name than the other args, and which does nothing.

        Returns:
            A dict mapping keys to the corresponding table row data
            fetched. Each row is represented as a tuple of strings. For
            example:

              {'Serak': ('Rigel VII', 'Preparer'),
               'Zim': ('Irk', 'Invader'),
               'Lrrr': ('Omicron Persei 8', 'Emperor')}

            If a key from the keys argument is missing from the dictionary,
            then that row was not found in the table.

        Raises:
            IOError: An error occurred accessing the bigtable.Table object.
        """

        expected = """        Fetches rows from a Bigtable.
        This is a continuation of the opening paragraph.

        Retrieves rows pertaining to the given keys from the Table instance
        represented by big_table.  Silly things may happen if
        other_silly_variable is not None.

        :param big_table: An open Bigtable Table instance.

        :param keys: A sequence of strings representing the key of each table row
            to fetch.

        :param other_silly_variable: Another optional variable, that has a much
            longer name than the other args, and which does nothing.

        :type other_silly_variable: str

        :returns: A dict mapping keys to the corresponding table row data
            fetched. Each row is represented as a tuple of strings. For
            example:

              {'Serak': ('Rigel VII', 'Preparer'),
               'Zim': ('Irk', 'Invader'),
               'Lrrr': ('Omicron Persei 8', 'Emperor')}

            If a key from the keys argument is missing from the dictionary,
            then that row was not found in the table.

        :raises:
            IOError - An error occurred accessing the bigtable.Table object.
        """
        source_lines = source.splitlines()
        actual_lines = parse_readabletext(source_lines)
        expected_lines = expected.splitlines()
        self.assertEqual(len(actual_lines), len(expected_lines))
        for actual_line, result_line in zip(actual_lines, expected_lines):
            if len(actual_line.strip()) == 0:
                self.assertTrue(len(result_line.strip()) == 0)
            else:
                self.assertEqual(actual_line, result_line)

    def test_comment2(self):
        source = """Determine if all elements in the source sequence satisfy a condition.

        All of the source sequence will be consumed.

        Note: This method uses immediate execution.

        Args:
            predicate: An optional single argument function used to test each
                elements. If omitted, the bool() function is used resulting in
                the elements being tested directly.

        Returns:
            True if all elements in the sequence meet the predicate condition,
            otherwise False.

        Raises:
            ValueError: If the Queryable is closed()
            TypeError: If predicate is not callable.
        """

        expected = """Determine if all elements in the source sequence satisfy a condition.

        All of the source sequence will be consumed.

        .. note::

            This method uses immediate execution.

        :param predicate: An optional single argument function used to test each
            elements. If omitted, the bool() function is used resulting in
            the elements being tested directly.

        :returns: True if all elements in the sequence meet the predicate condition,
            otherwise False.

        :raises:
            * ValueError - If the Queryable is closed()

            * TypeError - If predicate is not callable.
        """
        source_lines = source.splitlines()
        actual_lines = parse_readabletext(source_lines)
        expected_lines = expected.splitlines()
        self.assertEqual(len(actual_lines), len(expected_lines))
        for actual_line, result_line in zip(actual_lines, expected_lines):
            if len(actual_line.strip()) == 0:
                self.assertTrue(len(result_line.strip()) == 0)
            else:
                self.assertEqual(actual_line, result_line)

    def test_comment3(self):
        source = """Determine if all elements in the source sequence satisfy a condition.

        All of the source sequence will be consumed.

        Note: This method uses immediate execution.

        Args:
            predicate: An optional single argument function used to test each
                elements. If omitted, the bool() function is used resulting in
                the elements being tested directly.

        Returns:
            True if all elements in the sequence meet the predicate condition,
            otherwise False.

        Raises:
            ValueError: If the Queryable is closed()
            TypeError: If predicate is not callable.
        """

        expected = """Determine if all elements in the source sequence satisfy a condition.

        All of the source sequence will be consumed.

        .. note::

            This method uses immediate execution.

        :param predicate: An optional single argument function used to test each
            elements. If omitted, the bool() function is used resulting in
            the elements being tested directly.

        :returns: True if all elements in the sequence meet the predicate condition,
            otherwise False.

        :raises:
            * ValueError - If the Queryable is closed()

            * TypeError - If predicate is not callable.
        """
        source_lines = source.splitlines()
        actual_lines = parse_readabletext(source_lines)
        expected_lines = expected.splitlines()
        self.assertEqual(len(actual_lines), len(expected_lines))
        for actual_line, result_line in zip(actual_lines, expected_lines):
            if len(actual_line.strip()) == 0:
                self.assertTrue(len(result_line.strip()) == 0)
            else:
                self.assertEqual(actual_line, result_line)

    def test_comment4(self):
        source_lines = [u'Determine if all elements in the source sequence satisfy a condition.',
                        u'',
                        u'All of the source sequence will be consumed.',
                        u'',
                        u'Note: This method uses immediate execution.',
                        u'',
                        u'Args:',
                        u'    predicate: An optional single argument function used to test each',
                        u'        elements. If omitted, the bool() function is used resulting in',
                        u'        the elements being tested directly.',
                        u'',
                        u'Returns:',
                        u'    True if all elements in the sequence meet the predicate condition,',
                        u'    otherwise False.',
                        u'',
                        u'Raises:',
                        u'    ValueError: If the Queryable is closed()',
                        u'    TypeError: If predicate is not callable.',
                        u'']

        expected = """Determine if all elements in the source sequence satisfy a condition.

All of the source sequence will be consumed.

.. note::

    This method uses immediate execution.

:param predicate: An optional single argument function used to test each
    elements. If omitted, the bool() function is used resulting in
    the elements being tested directly.

:returns: True if all elements in the sequence meet the predicate condition,
    otherwise False.

:raises:
    * ValueError - If the Queryable is closed()

    * TypeError - If predicate is not callable.

"""
        actual_lines = parse_readabletext(source_lines)
        expected_lines = expected.splitlines()
        self.assertEqual(len(actual_lines), len(expected_lines))
        for actual_line, result_line in zip(actual_lines, expected_lines):
            if len(actual_line.strip()) == 0:
                self.assertTrue(len(result_line.strip()) == 0)
            else:
                self.assertEqual(actual_line, result_line)

    def test_comment5(self):
        source_lines = [u'An empty Queryable.',
                        u'',
                        u'Note: The same empty instance will be returned each time.',
                        u'',
                        u'Returns: A Queryable over an empty sequence.',
                        u'']

        expected = """An empty Queryable.

.. note::

    The same empty instance will be returned each time.

:returns: A Queryable over an empty sequence.

"""
        actual_lines = parse_readabletext(source_lines)
        expected_lines = expected.splitlines()
        self.assertEqual(len(actual_lines), len(expected_lines))
        for actual_line, result_line in zip(actual_lines, expected_lines):
            if len(actual_line.strip()) == 0:
                self.assertTrue(len(result_line.strip()) == 0)
            else:
                self.assertEqual(actual_line, result_line)

    def test_comment6(self):
        source_lines = [u'A convenience factory for creating Records.',
                        u'',
                        u'Args:',
                        u'    **kwargs: Each keyword argument will be used to initialise an',
                        u'       attribute with the same name as the argument and the given',
                        u'       value.',
                        u'',
                        u'Returns:',
                        u'    A Record which has a named attribute for each of the keyword arguments.',
                        u'']

        expected = """A convenience factory for creating Records.

:param **kwargs: Each keyword argument will be used to initialise an
   attribute with the same name as the argument and the given
   value.

:returns: A Record which has a named attribute for each of the keyword arguments.

"""
        actual_lines = parse_readabletext(source_lines)
        expected_lines = expected.splitlines()
        self.assertEqual(len(actual_lines), len(expected_lines))
        for actual_line, result_line in zip(actual_lines, expected_lines):
            if len(actual_line.strip()) == 0:
                self.assertTrue(len(result_line.strip()) == 0)
            else:
                self.assertEqual(actual_line, result_line)

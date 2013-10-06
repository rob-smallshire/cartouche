import unittest


from cartouche._portability import u
from cartouche.parser import (parse_cartouche_text, bulleted_raises, bulleted_args, CartoucheSyntaxError)

class IssueTests(unittest.TestCase):

    def test_issue1(self):
        source = """
        Bulleted arguments and exceptions.

        Args:
            * arg1: Argument 1.
            * arg2: Argument 2.

        Returns:
          Some value.

        Raises:
            * SomeError: If there is a problem.
            * AnotherError: If there's some other problem.
        """
        expected = """
        Bulleted arguments and exceptions.

        :param arg1: Argument 1.

        :param arg2: Argument 2.

        :returns: Some value.

        :raises:
            * SomeError - If there is a problem.

            * AnotherError - If there's some other problem.

"""
        with bulleted_args(), bulleted_raises():
            source_lines = source.splitlines()
            actual_lines = parse_cartouche_text(source_lines)
            expected_lines = expected.splitlines()
            self.assertEqual(len(actual_lines), len(expected_lines))
            for actual_line, result_line in zip(actual_lines, expected_lines):
                if len(actual_line.strip()) == 0:
                    self.assertTrue(len(result_line.strip()) == 0)
                else:
                    self.assertEqual(actual_line, result_line)

    def test_issue2(self):
        source = '''
A docstring.

Args:
  arg1: Some argument

Returns: Some kind of value.

Raises:
  exceptions.SomeError: There was some error.
'''

        expected = '''
A docstring.

:param arg1: Some argument

:returns: Some kind of value.

:raises:
  exceptions.SomeError - There was some error.

'''
        source_lines = source.splitlines()
        actual_lines = parse_cartouche_text(source_lines)
        expected_lines = expected.splitlines()
        self.assertEqual(len(actual_lines), len(expected_lines))
        for actual_line, result_line in zip(actual_lines, expected_lines):
            if len(actual_line.strip()) == 0:
                self.assertTrue(len(result_line.strip()) == 0)
            else:
                self.assertEqual(actual_line, result_line)


    def test_issue3(self):
        lines = [u('Parse a single line of a tree to determine depth and node.'),
                 u(''),
                 u('Args:'),
                 u('    A single line string from a SCons dependency tree.'),
                 u('    '),
                 u('Returns:'),
                 u('    A 2-tuple containing the tree 0 based tree depth as the first'),
                 u('    element and the node description as the second element.'),
                 u(''),
                 u('Raises:'),
                 u('    ValueError: If line does not have the expected form.'),
                 u('')]
        self.assertRaises(CartoucheSyntaxError, lambda: parse_cartouche_text(lines))

    def test_issue4(self):
        source = '''
    Execute the command described by concatenating the string function arguments
    with the p4 -s global scripting flag and return the results in a dictionary.

    For example, to run the command::

      p4 -s fstat -T depotFile foo.h

    call::

      p4('fstat', '-T', 'depotFile', 'foo.h')

    Args:
        args: The arguments to the p4 command as a list of objects which will
            be converted to strings.

    Returns:
        A dictionary of lists where each key in the dictionary is the field name
        from the command output, and each value is a list of output lines in
        order.

    Raises:
        PerforceError: If the command could not be run or if the command
            reported an error.
    '''

        source_lines = source.splitlines()

        try:
            parse_cartouche_text(source_lines)
        except UnboundLocalError:
            self.fail("parse_cartouche_text raised UnboundLocalError")

    def test_issue8(self):
        source = '''
A docstring.

Args:
  arg1 (some.type): Some argument
'''

        expected = '''
A docstring.

:param arg1: Some argument
:type arg1: some.type
'''
        source_lines = source.splitlines()
        actual_lines = parse_cartouche_text(source_lines)
        actual = "\n".join(actual_lines)
        self.assertEqual(expected, actual)

    def test_issue11(self):
        source = """
Raises:
Exception: This is a multi-line
bug.
"""
        source_lines = source.splitlines()
        parse_cartouche_text(source_lines)
        # We're just testing that this doesn't fail.

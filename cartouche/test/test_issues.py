import unittest

from cartouche.parser import (parse_cartouche_text, bulleted_raises, bulleted_args)

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

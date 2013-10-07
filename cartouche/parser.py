# -*- coding: utf-8 -*-
from __future__ import print_function
from contextlib import contextmanager

import re
from cartouche._portability import u

from .errors import CartoucheError

from .nodes import (Node, Raises, Except, Note, Warning, Returns, Arg, Yields,
                    Attribute, ensure_terminal_blank)

OPTIONAL_BULLET_PATTERN = u(r'(?:[\*\+\-\•\‣\⁃]\s+)?')
ARGS_PATTERN = u(r'(\*{0,2}\w+)(\s+\(([\.\w]+)\))?\s*:\s*(.*)')
ATTRIBUTES_PATTERN = u(r'(\*{0,2}\w+)(\s+\(([\.\w]+)\))?\s*:\s*(.*)')
RAISES_PATTERN = u(r'([\w\.]+)\s*:\s*(.*)')

ARGS_REGEX = re.compile(ARGS_PATTERN)
ATTRIBUTES_REGEX = re.compile(ATTRIBUTES_PATTERN)
RAISES_REGEX = re.compile(RAISES_PATTERN)

class CartoucheSyntaxError(CartoucheError):
    pass

def parse_cartouche_text(lines):
    '''Parse text in cartouche format and return a reStructuredText equivalent

    Args:
        lines: A sequence of strings representing the lines of a single
            docstring as read from the source by Sphinx. This string should be
            in a format that can be parsed by cartouche.

    Returns:
        A list of lines containing the transformed docstring as
        reStructuredText as produced by cartouche.

    Raises:
        RuntimeError: If the docstring cannot be parsed.
    '''
    indent_lines = unindent(lines)
    indent_lines = pad_blank_lines(indent_lines)
    indent_lines = first_paragraph_indent(indent_lines)
    indent_paragraphs = gather_lines(indent_lines)
    parse_tree = group_paragraphs(indent_paragraphs)
    syntax_tree = extract_structure(parse_tree)
    result = syntax_tree.render_rst()
    ensure_terminal_blank(result)
    return result


def unindent(lines):
    '''Convert an iterable of indented lines into a sequence of tuples.

    The first element of each tuple is the indent in number of characters, and
    the second element is the unindented string.

    Args:
        lines: A sequence of strings representing the lines of text in a docstring.

    Returns:
        A list of tuples where each tuple corresponds to one line of the input
        list. Each tuple has two entries - the first is an integer giving the
        size of the indent in characters, the second is the unindented text.
    '''
    unindented_lines = []
    for line in lines:
        unindented_line = line.lstrip()
        indent = len(line) - len(unindented_line)
        unindented_lines.append((indent, unindented_line))
    return unindented_lines


def pad_blank_lines(indent_texts):
    '''Give blank (empty) lines the same indent level as the preceding line.

    Args:
        indent_texts: An iterable of tuples each containing an integer in the
            first element and a string in the second element.

    Returns:
        A list of tuples each containing an integer in the first element and a
        string in the second element.
    '''
    current_indent = 0
    result = []
    for indent, text in indent_texts:
        if len(text) > 0:
            current_indent = indent
        result.append((current_indent, text))
    return result


def extract_structure(parse_tree):
    '''Create an Abstract Syntax Tree representing the semantics of a parse tree.

    Args:
        parse_tree: TODO

    Returns:
        A Node with is the result of an Abstract Syntax Tree representing the
        docstring.

    Raises:
        CartoucheError: In the event that the parse tree cannot be understood.
    '''
    return convert_node(parse_tree)


def convert_node(node):
    if node.indent == 0 and len(node.lines) == 0:
        return convert_children(node)
    if node.lines[0].startswith('Args:'):
        return convert_args(node)
    if node.lines[0].startswith('Returns:'):
        return convert_returns(node)
    if node.lines[0].startswith('Yields:'):
        return convert_yields(node)
    if node.lines[0].startswith('Raises:'):
        return convert_raises(node)
    if node.lines[0].startswith('Note:'):
        return convert_note(node)
    if node.lines[0].startswith('Warning:'):
        return convert_warning(node)
    if node.lines[0].startswith('Attributes:'):
        return convert_attributes(node)
    result = convert_children(node)
    result.lines = node.lines
    result.indent = node.indent
    return result


def convert_children(node):
    converted_children = [convert_node(child) for child in node.children]
    result = Node()
    result.children = converted_children
    return result


def append_child_to_args_group_node(child, group_node, indent):
    arg = None
    non_empty_lines = (line for line in child.lines if line)
    for line in non_empty_lines:
        m = ARGS_REGEX.match(line)
        if m is None:
            raise CartoucheSyntaxError('Cartouche: Invalid argument syntax "{line}" for Args block'.format(line=line))
        param_name = m.group(1)
        param_type = m.group(3)
        param_text = m.group(4)

        arg = Arg(indent, param_name)
        group_node.children.append(arg)
        arg.type = param_type

        if param_text is not None:
            arg.children.append(Node(indent, [param_text], arg))
    if arg is not None:
        last_child = arg.children[-1] if len(arg.children) != 0 else arg
        for grandchild in child.children:
            last_child.children.append(grandchild)


def append_child_to_attributes_group_node(child, group_node, indent):
    attribute = None
    non_empty_lines = (line for line in child.lines if line)
    for line in non_empty_lines:
        m = ATTRIBUTES_REGEX.match(line)
        if m is None:
            raise CartoucheSyntaxError('Cartouche: Invalid attribute syntax "{line}" for Attributes block'.format(line=line))
        attribute_name = m.group(1)
        attribute_type = m.group(3)
        attribute_text = m.group(4)

        attribute = Attribute(indent, attribute_name)
        group_node.children.append(attribute)
        attribute.type = attribute_type

        if attribute_text is not None:
            attribute.children.append(Node(indent, [attribute_text], attribute))
    if attribute is not None:
        last_child = attribute.children[-1] if len(attribute.children) != 0 else attribute
        for grandchild in child.children:
            last_child.children.append(grandchild)


def convert_args(node):
    assert node.lines[0].startswith('Args:')
    group_node = Node()
    for child in node.children:
        append_child_to_args_group_node(child, group_node, node.indent)
    return group_node


def convert_returns(node):
    assert node.lines[0].startswith('Returns:')
    returns = Returns(node.indent)
    returns.line = node.lines[0][8:].strip()
    returns.children = node.children
    return returns

def convert_yields(node):
    assert node.lines[0].startswith('Yields:')
    returns = Yields(node.indent)
    returns.line = node.lines[0][8:].strip()
    returns.children = node.children
    return returns

def convert_note(node):
    assert node.lines[0].startswith('Note:')
    note = Note(node.indent)
    note.line = node.lines[0][5:].strip()
    note.children = node.children
    return note


def convert_warning(node):
    assert node.lines[0].startswith('Warning:')
    warning = Warning(node.indent)
    warning.line = node.lines[0][8:].strip()
    warning.children = node.children
    return warning


def convert_raises(node):
    assert node.lines[0].startswith('Raises:')
    group_node = Raises(node.indent)
    for child in node.children:
        append_child_to_raise_node(child, group_node)
    return group_node


def convert_attributes(node):
    assert node.lines[0].startswith('Attributes:')
    group_node = Node()
    for child in node.children:
        append_child_to_attributes_group_node(child, group_node, node.indent)
    return group_node


def parse_exception(line):
    '''Parse the first line of a Cartouche exception description.

    Args:
        line (str): A single line Cartouche exception description.

    Returns:
        A 2-tuple containing the exception type and the first line of the description.
    '''
    m = RAISES_REGEX.match(line)
    if m is None:
        raise CartoucheSyntaxError('Cartouche: Invalid argument syntax "{line}" for Raises block'.format(line=line))
    return m.group(2), m.group(1)


def append_child_to_raise_node(child, group_node):
    exception = None
    non_empty_lines = (line for line in child.lines if line)
    for line in non_empty_lines:
        exception_text, exception_type = parse_exception(line)

        exception = Except(child.indent, exception_type)
        group_node.children.append(exception) # TODO: Could use parent here.

        if exception_text is not None:
            exception.children.append( Node(child.indent,
                                            [exception_text], exception))
    if exception is not None:
        last_child = exception.children[-1] if len(exception.children) != 0 else exception
        for grandchild in child.children:
            last_child.children.append(grandchild)


def group_paragraphs(indent_paragraphs):
    '''
    Group paragraphs so that more indented paragraphs become children of less
    indented paragraphs.
    '''
    # The tree consists of tuples of the form (indent, [children]) where the
    # children may be strings or other tuples

    root = Node(0, [], None)
    current_node = root

    previous_indent = -1
    for indent, lines in indent_paragraphs:
        if indent > previous_indent:
            current_node = create_child_node(current_node, indent, lines)
        elif indent == previous_indent:
            current_node = create_sibling_node(current_node, indent, lines)
        elif indent < previous_indent:
            current_node = create_uncle_node(current_node, indent, lines)
        previous_indent = indent
    return root


def create_sibling_node(current_node, indent, lines):
    sibling = Node(indent, lines, current_node.parent)
    current_node.parent.add_child(sibling)
    current_node = sibling
    return current_node


def create_child_node(current_node, indent, lines):
    child = Node(indent, lines, current_node)
    current_node.add_child(child)
    current_node = child
    return current_node


def create_uncle_node(current_node, indent, lines):
    ancestor = current_node
    while ancestor.indent >= indent:
        if ancestor.parent is None:
            break
        ancestor = ancestor.parent
    uncle = Node(indent, lines, ancestor)
    ancestor.add_child(uncle)
    current_node = uncle
    return current_node


def gather_lines(indent_lines):
    '''Split the list of (int, str) tuples into a list of (int, [str]) tuples
    to group the lines into paragraphs of consistent indent.
    '''
    return remove_empty_paragraphs(split_separated_lines(gather_lines_by_indent(indent_lines)))

def gather_lines_by_indent(indent_lines):
    result = []
    previous_indent = -1
    for indent, line in indent_lines:
        if indent != previous_indent:
            paragraph = (indent, [])
            result.append(paragraph)
        else:
            paragraph = result[-1]
        paragraph[1].append(line)
        previous_indent = indent
    return result

def split_separated_lines(indent_paragraphs):
    result = []
    for indent, paragraph in indent_paragraphs:
        result.append((indent, []))

        if len(paragraph) > 0:
            result[-1][1].append(paragraph[0])

        if len(paragraph) > 2:
            for line in paragraph[1: -1]:
                result[-1][1].append(line)
                if len(line) == 0:
                    result.append((indent, []))

        if len(paragraph) > 1:
            result[-1][1].append(paragraph[-1])

    return result

def remove_empty_paragraphs(indent_paragraphs):
    return [(indent, paragraph) for indent, paragraph in indent_paragraphs if len(paragraph)]

def first_paragraph_indent(indent_texts):
    '''Fix the indentation on the first paragraph.

    This occurs because the first line of a multi-line docstring following the
    opening quote usually has no indent.

    Args:
        indent_texts: The lines of the docstring as an iterable over 2-tuples
            each containing an integer indent level as the first element and
            the text as the second element.

    Return:
        A list of 2-tuples, each containing an integer indent level as the
        first element and the text as the second element.
    '''
    opening_indent = determine_opening_indent(indent_texts)

    result = []
    input = iter(indent_texts)
    for indent, text in input:
        if indent == 0:
            result.append((opening_indent, text))
        else:
            result.append((indent, text))
            break

    for indent, text in input:
        result.append((indent, text))

    return result


def determine_opening_indent(indent_texts):
    '''Determine the opening indent level for a docstring.

    The opening indent level is the indent level is the first non-zero indent
    level of a non-empty line in the docstring.

    Args:
        indent_texts: The lines of the docstring as an iterable over 2-tuples
            each containing an integer indent level as the first element and
            the text as the second element.

    Returns:
        The opening indent level as an integer.
    '''
    num_lines = len(indent_texts)

    if num_lines < 1:
        return 0

    assert num_lines >= 1

    first_line_indent  = indent_texts[0][0]

    if num_lines == 1:
        return first_line_indent

    assert num_lines >= 2

    second_line_indent = indent_texts[1][0]
    second_line_text   = indent_texts[1][1]

    if len(second_line_text) == 0:
        return first_line_indent

    return second_line_indent


#noinspection PyUnusedLocal
def rewrite_autodoc(app, what, name, obj, options, lines):
    '''Convert lines from Cartouche to Sphinx format.

    The function to be called by the Sphinx autodoc extension when autodoc
    has read and processed a docstring. This function modified its
    ``lines`` argument *in place* replacing Cartouche syntax input into
    Sphinx reStructuredText output.

    Args:
        apps: The Sphinx application object.

        what: The type of object which the docstring belongs to. One of
            'module', 'class', 'exception', 'function', 'method', 'attribute'

        name: The fully qualified name of the object.

        obj: The object itself.

        options: The options given to the directive. An object with attributes
            ``inherited_members``, ``undoc_members``, ``show_inheritance`` and
            ``noindex`` that are ``True`` if the flag option of the same name
            was given to the auto directive.

        lines: The lines of the docstring.  Will be modified *in place*.

    Raises:
        CartoucheSyntaxError: If the docstring is malformed.
    '''
    try:
        lines[:] = parse_cartouche_text(lines)
    except CartoucheSyntaxError as syntax_error:
        args = syntax_error.args
        arg0 = args[0] if args else ''
        arg0 += " in docstring for {what} {name} :".format(what=what, name=name)
        arg0 += "\n=== BEGIN DOCSTRING ===\n{lines}\n=== END DOCSTRING ===\n".format(lines='\n'.join(lines))
        #noinspection PyPropertyAccess
        syntax_error.args = (arg0,) + args[1:]
        raise


def accept_bulleted_args():
    '''Further use of the parser will accept bulleted lists for Args.'''
    global ARGS_REGEX
    ARGS_REGEX = re.compile(OPTIONAL_BULLET_PATTERN + ARGS_PATTERN)


def reject_bulleted_args():
    '''Further use of the parser will reject bulleted lists for Args.'''
    global ARGS_REGEX
    ARGS_REGEX = re.compile(ARGS_PATTERN)


def accept_bulleted_raises():
    '''Further use of the parser will accept bulleted lists for Raises.'''
    global RAISES_REGEX
    RAISES_REGEX = re.compile(OPTIONAL_BULLET_PATTERN + RAISES_PATTERN)


def reject_bulleted_raises():
    '''Further use of the parser will reject bulleted lists for Raises.'''
    global RAISES_REGEX
    RAISES_REGEX = re.compile(RAISES_PATTERN)


@contextmanager
def bulleted_args():
    '''A context manager within the scope of which bulleted Args will be accepted.'''
    global ARGS_REGEX
    previous_args_regex = ARGS_REGEX
    accept_bulleted_args()
    yield
    ARGS_REGEX = previous_args_regex


@contextmanager
def bulleted_raises():
    '''A context manager within the scope of which bulleted Raises will be accepted.'''
    global RAISES_REGEX
    previous_raises_regex = RAISES_REGEX
    accept_bulleted_raises()
    yield
    RAISES_REGEX = previous_raises_regex


def builder_inited(app):
    if app.config.cartouche_accept_bulleted_args:
        accept_bulleted_args()

    if app.config.cartouche_accept_bulleted_raises:
        accept_bulleted_raises()






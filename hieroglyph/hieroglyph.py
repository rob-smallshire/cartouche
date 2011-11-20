import re
import sys

from errors import HieroglyphError
from nodes import (Node, Raises, Except, Note, Warning, Returns, Arg,
                   ensure_terminal_blank)

__author__ = 'Robert Smallshire'

def parse_readabletext(lines):
    '''Parse text in hieroglyph format and return a reStructuredText equivalent

    Args:
        lines: A sequence of strings representing the lines of one docstring as
            read from the source by Sphinx. This string should be in a format
            that can be parsed by hieroglyph.

    Returns:
        A list of lines containing the transformed docstring as
        reStructuredText as produced by hieroglyph.

    Raises:
        RuntimeError: If the docstring cannot be parsed.
    '''
    # In the event of failure - we could consider catching a specific
    # HieroglyphError here and returning the original lines untransformed -
    # that would be a good solution if we could also figure out how to signal
    # the error to Sphinx so that the problem is reported to the user.
    try:
        indent_lines = unindent(lines)
        indent_lines = pad_blank_lines(indent_lines)
        indent_lines = first_paragraph_indent(indent_lines)
        indent_paragraphs = split_paragraphs(indent_lines)
        parse_tree = group_paragraphs(indent_paragraphs)
        syntax_tree = extract_structure(parse_tree)
        result = syntax_tree.render_rst()
        ensure_terminal_blank(result)
    except HieroglyphError as e:
        sys.stderr.write("Hieroglyph error: ")
        sys.stderr.write(str(e))
        sys.stderr.write('\n')
        result = lines
    return result


def extract_structure(node):
    return convert_node(node)


def convert_node(node):
    if node.indent == 0 and len(node.lines) == 0:
        return convert_children(node)
    if node.lines[0].startswith('Args:'):
        return convert_args(node)
    if node.lines[0].startswith('Returns:'):
        return convert_returns(node)
    if node.lines[0].startswith('Raises:'):
        return convert_raises(node)
    if node.lines[0].startswith('Note:'):
        return convert_note(node)
    if node.lines[0].startswith('Warning:'):
        return convert_warning(node)
    result = convert_children(node)
    result.lines = node.lines
    result.indent = node.indent
    return result


def convert_children(node):
    converted_children = [convert_node(child) for child in node.children]
    result = Node()
    result.children = converted_children
    return result


ARG_REGEX = re.compile(r'(\*{0,2}\w+)(\s+\((\w+)\))?\s*:\s*(.*)')

def append_child_to_args_group_node(child, group_node, indent):
    arg = None
    non_empty_lines = (line for line in child.lines if line)
    for line in non_empty_lines:
        m = ARG_REGEX.match(line)
        if m is None:
            raise HieroglyphError("Invalid hieroglyph argument syntax")
        param_name = m.group(1)
        param_type = m.group(3)
        param_text = m.group(4)

        arg = Arg(indent, child.indent, param_name)
        group_node.children.append(arg)
        arg.type = param_type

        if param_text is not None:
            arg.children.append(Node(indent, [param_text], arg))
    if arg is not None:
        last_child = arg.children[-1] if len(arg.children) != 0 else arg
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


RAISE_REGEX = re.compile(r'(\w+)\s*:\s*(.*)')

def append_child_to_raise_node(child, group_node):
    exception = None
    non_empty_lines = (line for line in child.lines if line)
    for line in non_empty_lines:
        m = RAISE_REGEX.match(line)
        if m is None:
            raise HieroglyphError("Invalid hieroglyph exception syntax")
        exception_type = m.group(1)
        exception_text = m.group(2)

        exception = Except(group_node.indent, child.indent, exception_type)
        group_node.children.append(exception)

        if exception_text is not None:
            exception.children.append( Node(group_node.indent,
                                            [exception_text], exception))
    if exception is not None:
        last_child = exception.children[-1] if len(
            exception.children) != 0 else exception
        for grandchild in child.children:
            last_child.children.append(grandchild)


def group_paragraphs(indent_paragraphs):
    '''
    Group paragraphs so that more indented paragraphs become children of less
    indented paragraphs.
    '''
    # The three consists of tuples of the form (indent, [children]) where the
    # children may be strings or other tuples

    root = Node(0, [], None)
    current_node = root

    current_indent = -1
    for indent, lines in indent_paragraphs:
        if indent > current_indent:
            # Child
            child = Node(indent, lines, current_node)
            current_node.add_child(child)
            current_node = child
        elif indent == current_indent:
            # Sibling
            sibling = Node(indent, lines, current_node.parent)
            current_node.parent.add_child(sibling)
            current_node = sibling
        elif indent < current_indent:
            # (Great) Uncle
            ancestor = current_node
            while ancestor.indent >= indent:
                if ancestor.parent is None:
                    break
                ancestor = ancestor.parent
            uncle = Node(indent, lines, ancestor)
            ancestor.add_child(uncle)
            current_node = uncle
        current_indent = indent
    return root


def split_paragraphs(indent_lines):
    '''Split the list of (int, str) tuples into a list of (int, [str]) tuples
    to group the lines into paragraphs of consistent indent.
    '''
    result = []
    previous_indent = -1
    previous_blank = False
    new_para = False
    for indent, line in indent_lines:
        blank = len(line) == 0
        indented = indent != previous_indent
        new_para = previous_blank or indented or new_para
        if True: #len(line) > 0:
            if new_para:
                paragraph = (indent, [])
                result.append(paragraph)
                new_para = False
            else:
                paragraph = result[-1]
            paragraph[1].append(line)
        previous_indent = indent
        previous_blank = blank

    return result


def first_paragraph_indent(indent_texts):
    '''Fix the indentation on the first paragraph. This occurs because the first
    line of a multi-line doc-string following a quote usually has no indent.
    '''
    result = indent_texts[:]
    current_indent = 0
    for indent, text in indent_texts:
        if len(text) == 0:
            break
        current_indent = indent

    if len(result) != 0:
        result[0] = (current_indent, result[0][1])

    return result


def pad_blank_lines(indent_texts):
    '''Give blank lines the same indent level as the preceding line.'''
    current_indent = 0
    result = []
    for indent, text in indent_texts:
        if len(text) > 0:
            current_indent = indent
        result.append((current_indent, text))
    return result


def unindent(lines):
    '''Convert a sequence of indented lines into a sequence of tuples where the
    first element in each tuple is the indent in number of characters, and the
    second element is the un-indented string'''
    unindented_lines = []
    for line in lines:
        unindented_line = line.lstrip()
        indent = len(line) - len(unindented_line)
        unindented_lines.append((indent, unindented_line))
    return unindented_lines


def rewrite_autodoc(app, what, name, obj, options, lines):
    copy = lines[:]
    try:
        lines[:] = parse_readabletext(lines)
    except:
        print "lines =", copy
        raise


def setup(app):
    app.connect('autodoc-process-docstring', rewrite_autodoc)



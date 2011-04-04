import re

__author__ = 'rjs'

def ensure_terminal_blank(result):
    '''If the description didn't end with a blank line add one here.'''
    if len(result) > 0:
        if len(result[-1].strip()) != 0:
            result.append('')

def parse_readabletext(lines):
    '''
    Parse text in hieroglyph format and return a reStructuredText sphinx
    equivalent,
    '''
    # Label each line with it's indent level and remove that indent prefix
    indent_lines = unindent(lines)
    indent_lines = pad_blank_lines(indent_lines)
    indent_lines = first_paragraph_indent(indent_lines)
    indent_paragraphs = split_paragraphs(indent_lines)
    parse_tree = group_paragraphs(indent_paragraphs)
    syntax_tree = extract_structure(parse_tree)
    result = syntax_tree.render_rst()
    ensure_terminal_blank(result)
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

arg_regex = re.compile(r'(\*{0,2}\w+)(\s+\((\w+)\))?\s*:\s*(.*)')

def convert_args(node):
    assert node.lines[0].startswith('Args:')
    group_node = Node()
    for child in node.children:
        arg = None
        for line in child.lines:
            m = arg_regex.match(line)
            if m is not None:
                param_name = m.group(1)
                param_type = m.group(3)
                param_text = m.group(4)

                arg = Arg(node.indent, child.indent, param_name)
                group_node.children.append(arg)
                arg.type = param_type

                if param_text is not None:
                    arg.children.append(Node(node.indent, [param_text], arg))
            else:
                #TODO: arg.children.append(line)
                pass
        if arg is not None:
            last_child = arg.children[-1] if len(arg.children) != 0 else arg
            for grandchild in child.children:
                last_child.children.append(grandchild)
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

raise_regex = re.compile(r'(\w+)\s*:\s*(.*)')

def convert_raises(node):
    assert node.lines[0].startswith('Raises:')
    group_node = Raises(node.indent)
    for child in node.children:
        exception = None
        for line in child.lines:
            m = raise_regex.match(line)
            if m is not None:
                exception_type = m.group(1)
                exception_text = m.group(2)

                exception = Except(node.indent, child.indent, exception_type)
                group_node.children.append(exception)

                if exception_text is not None:
                    exception.children.append(Node(node.indent, [exception_text], exception))
            else:
                #TODO: exception.children.append(line)
                pass
        if exception is not None:
            last_child = exception.children[-1] if len(exception.children) != 0 else exception
            for grandchild in child.children:
                last_child.children.append(grandchild)
    return group_node


class Node(object):

    def __init__(self, indent=None, lines=None, parent=None):
        if indent is not None:
            self.indent = indent
        else:
            self.indent = 0

        if lines is not None:
            self.lines = lines
        else:
            self.lines = []

        self.parent = parent

        self.children = []

    def add_child(self, child):
        assert(child.parent is self)
        self.children.append(child)

    def __repr__(self):
        return "Node(" + str(self.indent) + ", " + str(self.lines) + ", children=" + str(self.children) + ")"

    def render_rst(self):
        result = []
        prefix = ' ' * self.indent
        result.extend(prefix + line for line in self.lines)
        for child in self.children:
               result.extend(child.render_rst())
        return result


class Arg(Node):

    def __init__(self, indent, child_indent, name):
        super(Arg, self).__init__(indent)
        self.child_indent = child_indent
        self.name = name
        self.type = None
        self.children = []

    def __repr__(self):
        return "Arg(" + str(self.name) + ", " + str(self.type) + ", children=" + str(self.children) + ")"

    def render_rst(self):
        result = []
        indent = ' ' * self.indent

        # Render the param description
        description = []
        for child in self.children:
            child_lines = child.render_rst()
            description.extend(child_lines)

        dedent = self.child_indent - self.indent

        name = self.name.replace('*', r'\*')

        result.append("{indent}:param {name}: {first_description}".format(indent=indent, name=name,
                        first_description=description[0].lstrip()))

        dedented_body = [line[dedent:] for line in description[1:]]

        result.extend(dedented_body)

        ensure_terminal_blank(result)

        # If a type was specified render the type
        if self.type is not None:
            result.append("{indent}:type {name}: {type}".format(indent=indent, name=self.name, type=self.type))
            result.append('')
        return result


class Raises(Node):

    def __repr__(self):
        return "Raises(" + str(self.indent) + ", " + str(self.lines) + ", children=" + str(self.children) + ")"

    def render_rst(self):
        result = []
        prefix = ' ' * self.indent
        result.append(prefix + ':raises:')
        # TODO: result.extend(prefix + line for line in self.lines)
        for child in self.children:
            result.extend(child.render_rst(only_child=len(self.children) == 1))

        # If the description didn't end with a blank line add one here
        if len(result[-1].strip()) != 0:
            result.append('')

        return result


class Except(Node):

    def __init__(self, indent, child_indent, type):
        super(Except, self).__init__(indent=indent)
        self.child_indent = child_indent
        self.type = type
        self.children = []

    def __repr__(self):
        return "Except(" + str(self.type) + ", children=" + str(self.children) + ")"

    def render_rst(self, only_child=False):
        result = []
        indent = ' ' * self.child_indent

        # Render the param description
        description = []
        for child in self.children:
            child_lines = child.render_rst()
            description.extend(child_lines)

        dedent = self.child_indent - self.indent

        bullet = '* ' if not only_child else ''

        result.append("{indent}{bullet}{type} - {first_description}".format(indent=indent,
                        bullet=bullet, type=self.type,
                        first_description=description[0].lstrip()))

        dedented_body = [line[dedent:] for line in description[1:]]

        result.extend(dedented_body)

        # If the description didn't end with a blank line add one here
        if len(result[-1].strip()) != 0:
            result.append('')

        return result

class TitleNode(Node):

    def __init__(self, title, indent):
        super(TitleNode, self).__init__(indent=indent)
        self.title = title
        self.line = ''
        self.children = []

    def __repr__(self):
        return self.title + "(children=" + str(self.children) + ")"

    def render_rst(self):
        result = []
        indent = ' ' * self.indent

        # Render the param description
        description = [self.line] if self.line else []
        for child in self.children:
            child_lines = child.render_rst()
            description.extend(child_lines)

        self.render_title(description, indent, result)

        result.extend(description[1:])

        # If the description didn't end with a blank line add one here
        if len(result[-1].strip()) != 0:
            result.append('')
        return result

    def render_title(self, description, indent, result):
        result.append(
            "{indent}:{role}: {first_description}".format(indent=indent,
               role=self.title.lower(), first_description=description[0].lstrip()))

class Returns(TitleNode):

    def __init__(self, indent):
        super(Returns, self).__init__(title='Returns', indent=indent)

class Warning(TitleNode):

    def __init__(self, indent):
        super(Warning, self).__init__(title='Warning', indent=indent)

class Note(Node):

    def __init__(self, indent):
        super(Note, self).__init__(indent=indent)
        self.line = ''

    def __repr__(self):
        return "Note(children=" + str(self.children) + ")"

    def render_rst(self):
        result = []
        indent = ' ' * self.indent

        # Render the param description
        description = [self.line] if self.line else []
        for child in self.children:
            child_lines = child.render_rst()
            description.extend(child_lines)

        # Fix the indent on the first line
        if len(description) > 1 and len(description[1].strip()) != 0:
            body_indent = len(description[1]) - len(description[1].strip())
        else:
            body_indent = self.indent + 4

        if len(description) > 0:
            description[0] = ' ' * body_indent + description[0]

        result.append(indent + ".. note::")
        result.append(indent + '')
        result.extend(description)

        # If the description didn't end with a blank line add one here
        if len(result[-1].strip()) != 0:
            result.append('')
        return result


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
    try:
        copy = lines[:]
        lines[:] = parse_readabletext(lines)
    except:
        print "lines =", copy
        raise

def setup(app):
    app.connect('autodoc-process-docstring', rewrite_autodoc)



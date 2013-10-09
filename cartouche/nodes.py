from __future__ import print_function

__author__ = 'Robert Smallshire'
import sys

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

        self._parent = parent

        self.children = []

    parent = property(lambda self: self._parent)

    def add_child(self, child):
        assert(child.parent is self)
        self.children.append(child)

    def __repr__(self):
        return "Node(" + repr(self.indent) + ", " + repr(self.lines)\
                       + ", children=" + repr(self.children) + ")"

    def render_rst(self, *args, **kwargs):
        result = []
        prefix = ' ' * self.indent
        result.extend(prefix + line for line in self.lines)
        for child in self.children:
            result.extend(child.render_rst())
        return result


class Arg(Node):

    def __init__(self, indent, name):
        super(Arg, self).__init__(indent)
        self.name = name
        self.type = None

    def __repr__(self):
        return "Arg(" + repr(self.name) + ", " + repr(self.type) + ", children=" + repr(self.children) + ")"

    def render_rst(self, *args, **kwargs):
        result = []
        indent = ' ' * self.indent

        # Render the param description
        description = []
        for child in self.children:
            child_lines = child.render_rst()
            description.extend(child_lines)

        name = self.name.replace('*', r'\*')

        first_description = description[0].lstrip() if len(description) else ''
        if not first_description:
            print("Missing argument description for {name}".format(name=self.name), file=sys.stderr)

        result.append("{indent}:param {name}: {first_description}".format(
                        indent=indent, name=name,
                        first_description=first_description))

        result.extend(description[1:])

        # If a type was specified render the type
        if self.type is not None:
            result.append("{indent}:type {name}: {type}".format(indent=indent,
                                             name=self.name, type=self.type))
            result.append('')

        ensure_terminal_blank(result)

        return result

class Attribute(Node):

    def __init__(self, indent, name):
        super(Attribute, self).__init__(indent)
        self.name = name
        self.type = None


    def __repr__(self):
        return "Attribute(" + repr(self.name) + ", " + repr(self.type)\
                            + ", children=" + repr(self.children) + ")"


    def render_rst(self, *args, **kwargs):
        result = []
        indent = ' ' * self.indent

        # Render the attribute description
        description = []
        for child in self.children:
            child_lines = child.render_rst()
            description.extend(child_lines)

        if self.type is not None:
            if len(description) > 0:
                description[0] = "({t}) {desc}".format(
                    t=self.type, desc=description[0].lstrip())
            else:
                description = ["({t})".format(t=self.type)]

        # The description lines should be indented by three characters to line
        # up with the directive.
        reindented_description = ["   " + line.lstrip() for line in description]

        result.append(".. py:attribute:: {name}".format(name=self.name))

        if len(reindented_description) > 0:
            result.append('')
            result.extend(reindented_description)

        ensure_terminal_blank(result)

        return result

class Raises(Node):

    def __init__(self, indent=None):
        super(Raises, self).__init__(indent=indent)

    def __repr__(self):
        return "Raises(" + repr(self.indent) + ", children=" + repr(self.children) + ")"


    def render_rst(self, *args, **kwargs):
        result = []
        indent = ' ' * self.indent
        result.append(indent + ':raises:')
        for child in self.children:
            result.extend(child.render_rst(only_child=len(self.children) == 1))

        ensure_terminal_blank(result)

        return result


class Except(Node):

    def __init__(self, indent, type):
        super(Except, self).__init__(indent=indent)
        #self.child_indent = child_indent
        self.type = type

    def __repr__(self):
        return "Except(" + repr(self.type) + ", children="\
                         + repr(self.children) + ")"

    def render_rst(self, only_child=False, *args, **kwargs):
        result = []
        indent = ' ' * self.indent

        # Render the param description
        description = []
        for child in self.children:
            child_lines = child.render_rst()
            description.extend(child_lines)

        bullet = '* ' if not only_child else ''

        first_description = description[0].lstrip() if len(description) else ''
        if not first_description:
            # TODO: Emit a warning about a missing argument description
            pass
        result.append("{indent}{bullet}{type} - {first_description}".format(
                        indent=indent,
                        bullet=bullet, type=self.type,
                        first_description=first_description))

        result.extend(description[1:])
        ensure_terminal_blank(result)

        return result


class Returns(Node):

    def __init__(self, indent):
        super(Returns, self).__init__(indent=indent)
        self.title = 'Returns'
        self.line = ''

    def __repr__(self):
        return "Returns(" + str(self.indent) + ", children=" + str(self.children) + ")"

    def render_rst(self, *args, **kwargs):
        result = []
        indent = ' ' * self.indent

        # Render the return description
        description = [self.line] if self.line else []
        for child in self.children:
            child_lines = child.render_rst()
            description.extend(child_lines)

        self.render_title(description, indent, result)

        result.extend(description[1:])

        ensure_terminal_blank(result)
        return result

    def render_title(self, description, indent, result):
        first_description = description[0].lstrip() if len(description) else ''
        result.append(
            "{indent}:returns: {first_description}".format(indent=indent,
               first_description=first_description))


class Yields(Node):

    def __init__(self, indent):
        super(Yields, self).__init__(indent=indent)
        self.title = 'Returns'
        self.line = ''


    def __repr__(self):
        return "Yields(" + str(self.indent) + ", children=" + str(self.children) + ")"


    def render_rst(self, *args, **kwargs):
        result = []
        indent = ' ' * self.indent

        # Render the return description
        description = [self.line] if self.line else []
        for child in self.children:
            child_lines = child.render_rst()
            description.extend(child_lines)

        self.render_title(description, indent, result)

        result.extend(description[1:])

        ensure_terminal_blank(result)
        return result


    def render_title(self, description, indent, result):
        first_description = description[0].lstrip() if len(description) else ''
        result.append(
            "{indent}:returns: {first_description}".format(indent=indent,
                first_description=first_description))


class Warning(Node):

    def __init__(self, indent):
        super(Warning, self).__init__(indent=indent)
        self.line = '' # TODO: Can't we use self.lines in the superclass for this?

    def __repr__(self):
        return "Warning(" + repr(self.indent) + ", children=" + str(self.children) + ")"

    def render_rst(self, *args, **kwargs):
        # TODO: Factor out the commonality between this and Note below
        result = []
        indent = ' ' * self.indent

        # Render the param description
        description = [indent + '    ' + self.line] if self.line else []
        for child in self.children:
            child_lines = child.render_rst()
            description.extend(child_lines)

        result.append(indent + ".. warning::")
        result.append(indent + '')
        result.extend(description)

        ensure_terminal_blank(result)
        return result


class Note(Node):

    def __init__(self, indent):
        super(Note, self).__init__(indent=indent)
        self.line = ''  # TODO: Can't we use self.lines in the superclass for this?

    def __repr__(self):
        return "Note(" + repr(self.indent) + ", children=" + str(self.children) + ")"

    def render_rst(self, *args, **kwargs):
        # TODO: Factor out the commonality between this and Warning above
        result = []
        indent = ' ' * self.indent

        # Render the param description
        description = [indent + '    ' + self.line] if self.line else []
        for child in self.children:
            child_lines = child.render_rst()
            description.extend(child_lines)

        result.append(indent + ".. note::")
        result.append(indent + '')
        result.extend(description)

        ensure_terminal_blank(result)
        return result

class Usage(Node):

    def __init__(self, indent):
        super(Usage, self).__init__(indent=indent)
        self.line = ''  # TODO: Can't we use self.lines in the superclass for this?
        self.lang = 'python'

    def __repr__(self):
        return "Usage(" + repr(self.indent) + ")"

    def render_rst(self, *args, **kwargs):
        result = []
        indent = ' ' * self.indent

        # Render the param description
        description = []
        for child in self.children:
            child_lines = child.render_rst()
            description.extend(child_lines)

        if len(description) > 0:
            minimum_code_indent = min(len(codeline) - len(codeline.lstrip()) for codeline in description if not codeline.isspace())
            codelines = [codeline[minimum_code_indent:] for codeline in description]

            result.append(indent + ".. rubric:: Usage:")
            result.append('')
            result.append(indent + '.. code-block:: {lang}'.format(lang=self.lang))
            result.append('')
            for codeline in codelines:
                result.append(indent + '   ' + codeline)
        else:
            print("No code in Usage block. Skipping!", file=sys.stderr)

        ensure_terminal_blank(result)
        return result

def ensure_terminal_blank(result):
    '''If the description didn't end with a blank line add one here.'''
    if len(result) > 0:
        if len(result[-1].strip()) != 0:
            result.append('')

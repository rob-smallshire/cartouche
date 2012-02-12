__author__ = 'Robert Smallshire'

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

    #indent = property(lambda self: return self._indent)

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
        indent = ' ' * self.indent
        result.append(indent + ':raises:')
        for child in self.children:
            result.extend(child.render_rst(only_child=len(self.children) == 1))

        ensure_terminal_blank(result)

        return result


class Except(Node):

    def __init__(self, indent, child_indent, type):
        super(Except, self).__init__(indent=indent)
        self.child_indent = child_indent
        self.type = type


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

        dedented_body = [' ' * len(bullet) + line[dedent:] for line in description[1:]]

        result.extend(dedented_body)

        ensure_terminal_blank(result)

        return result



class TitleNode(Node):

    def __init__(self, title, indent):
        super(TitleNode, self).__init__(indent=indent)
        self.title = title
        self.line = ''


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

        ensure_terminal_blank(result)
        return result


    def render_title(self, description, indent, result):
        result.append(
            "{indent}:{role}: {first_description}".format(indent=indent,
               role=self.title.lower(), first_description=description[0].lstrip()))



class Returns(TitleNode):

    def __init__(self, indent):
        super(Returns, self).__init__(title='Returns', indent=indent)



class Warning(Node):

    def __init__(self, indent):
        super(Warning, self).__init__(indent=indent)

    def __repr__(self):
        return "Warning(children=" + str(self.children) + ")"

    def render_rst(self):
        # TODO: Factor out the commonality between this and Note below
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

        result.append(indent + ".. warning::")
        result.append(indent + '')
        result.extend(description)

        ensure_terminal_blank(result)
        return result


class Note(Node):

    def __init__(self, indent):
        super(Note, self).__init__(indent=indent)
        self.line = ''


    def __repr__(self):
        return "Note(children=" + str(self.children) + ")"


    def render_rst(self):
        # TODO: Factor out the commonality between this and Warning above
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

        ensure_terminal_blank(result)
        return result


def ensure_terminal_blank(result):
    '''If the description didn't end with a blank line add one here.'''
    if len(result) > 0:
        if len(result[-1].strip()) != 0:
            result.append('')

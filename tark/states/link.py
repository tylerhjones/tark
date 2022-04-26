from . import State


class Link(State):
    def __init__(self):
        super().__init__()
        self.name = 'Link'

    def parse(self, stack):
        text = LinkText().parse(stack)
        link = LinkUrl().parse(stack)
        return f"<a href='{link}'>{text}</a>"


class LinkText(State):
    def __init__(self):
        super().__init__()
        self.name = 'LinkText'

    def parse(self, stack):
        stack.pop() # drop open bracket
        tokens = stack.seek_until(lambda tok: tok.type == 'CloseBracket')
        tokens.pop() # drop close bracket
        return ''.join([t.value for t in tokens])


class LinkUrl(State):
    def __init__(self):
        super().__init__()
        self.name = 'LinkUrl'

    def parse(self, stack):
        stack.pop() # drop open parenthesis
        tokens = stack.seek_until(lambda tok: tok.type == 'CloseParen')
        tokens.pop() # drop close bracket
        return ''.join([t.value for t in tokens])
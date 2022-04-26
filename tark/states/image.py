from . import State
from .link import LinkUrl
from .link import LinkText

class Image(State):
    def __init__(self):
        self.name = 'Image'
        super().__init__()

    def parse(self, stack):
        stack.pop() # drop the bang
        text = LinkText().parse(stack)
        link = LinkUrl().parse(stack)
        return f"<img src='{link}' alt='{text}'>"
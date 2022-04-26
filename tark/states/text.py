from . import State
from .inlinecode import InlineCode
from .link import Link
from .image import Image
class Text(State):
    def __init__(self):
        super().__init__()
        self.name = 'Text'
    def parse(self, stack):
        exit = False
        while not stack.is_empty():
            token = stack.peek()
            match token.type:
                case 'OpenBracket': self.buffer += Link().parse(stack)
                case 'Tick': self.buffer += InlineCode().parse(stack)
                case 'Bang': self.buffer += Image().parse(stack)
                case 'Escape': self.buffer += stack.pop(n=2)[1].value # append next as literal
                case 'Newline':
                    stack.pop() # drop and return
                    return self.buffer
                case _: 
                    print("default")
                    self.buffer += stack.pop().value
        return self.buffer
from . import State
from .title import Title
from .tick import Tick


class Plain(State):
    '''
    This is the root state in the AST.
    '''
    def __init__(self):
        super().__init__()
        self.name = 'Plain'
    
    def parse(self, stack):
        while not stack.is_empty():
            token = stack.peek()

            # todo: this will choke when token in middle of text
            # eg. "this is not # a title"
            match token.type: 
                case 'Octo': self.buffer += Title().parse(stack)
                case 'Tick': self.buffer += Tick().parse(stack)
                case _: self.buffer += stack.pop().value
        return self.buffer
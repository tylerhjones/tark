from . import State
from .inlinecode import InlineCode
from .codeblock import CodeBlock

class Tick(State):
    def __init__(self):
        self.name = 'Tick'
        super().__init__()

    def parse(self, stack):
        token = stack.peek()

        match token.value:
            case '`':
                return InlineCode().parse(stack)
            case '```':
                return CodeBlock().parse(stack)
            case _:
                raise Exception('Tick length must be 1 or 3')
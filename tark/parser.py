from .structures import Stack
from .states import Title, Tick, Text
class Parser:
    '''
    BNF
    <Plain> ::= Text | Title | CodeBlock | InlineCode
    <Text> ::= InlineCode | Link | Tick | Text
    <Title> ::= Octo, Space, Text, Newline
    <CodeBlock> ::= Tick, Newline, ANY+, Newline, Tick, Newline
    '''
    def parse(self, tokens):
        stack = Stack(tokens)
        if stack.stack[0].type != 'Newline':
            raise Exception("Tark files must end in a newline")
        document = []
        try:
            while not stack.is_empty():
                token = stack.peek()
                match token.type:
                    case 'Octo': document.append(Title().parse(stack))
                    case 'Tick': document.append(Tick().parse(stack))
                    case 'Text': document.append("<div>"+Text().parse(stack)+"</div>")
                    case 'Newline': document.append(stack.pop().value) # out of context newline
                    case 'Space': document.append(stack.pop().value) # out of context space
                    case 'Digit': document.append(stack.pop().value) # out of context digit
                    case _: raise Exception('Unexpected token type {}'.format(token.type))
            return ''.join(document)
        except Exception as e:
            raise Exception(f"Parse error at [{stack.line},{stack.row}]\n", e)
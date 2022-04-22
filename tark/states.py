import string
import re

class State:
    def __init__(self):
        self.buffer = ''
    
class Text(State):
    def __init__(self):
        super().__init__()
        self.name = 'Text'

    def parse(self, stack):
        return stack.pop().value

class Title(State):
    def __init__(self):
        self.name = 'Octo'
        super().__init__()

    def parse(self, stack):
        # first tokens are Octo+, Space
        token = stack.pop()
        size = len(token.value)
        if size > 6:
            raise Exception('Octo title cannot be greater than size 6')
        if '#'*size != token.value:
            raise Exception('Octo title must be a series of #')

        token = stack.pop() # dump the space
        if token.type != 'Space':
            raise Exception('Octo title must be followed by a space')
        
        tokens = stack.seek_until(lambda tok: tok.value.startswith('\n\n'))
        l = len(tokens)
        tokens = tokens[:l-1] # remove the final newline

        self.buffer += f"<h{size}>"
        self.buffer += ''.join([t.value for t in tokens])
        self.buffer += f"</h{size}>"
        return self.buffer

class CodeBlock(State):
    def __init__(self):
        self.name = 'CodeBlock'
        super().__init__()
        self.valid_language_chars = list(string.ascii_lowercase)

    def parse(self, stack):
        tokens = stack.pop(n=3)
        opening = ''.join([t.value for t in tokens])
        if not re.match(r'^```[a-z]+\n$', opening):
            raise Exception(
                'Code block must start with ``` and specify language ending in newline. \nwas {}'.format(tokens))

        language = tokens[1].value # the language is the second token
        # todo: a second language specific parse to break up the code into elements
        tokens = stack.seek_until(lambda tok: tok.value.startswith('```'))
        tokens = tokens[:len(tokens)-1] # remove the final ```

        self.buffer += f"<pre class=\"code_block\"><code class=\"{language}\">"
        self.buffer += ''.join([t.value for t in tokens])
        self.buffer += '</code></pre>'
        return self.buffer

class InlineCode(State):
    def __init__(self):
        self.name = 'InlineCode'
        super().__init__()

    def parse(self, stack):
        tik = stack.pop() # drop first tick
        if tik.value != '`':
            raise Exception('Inline code must start with a tick')

        # We seek until the next tick. 
        # This will terminate the inline code no matter the number of ticks
        # eg. `this is inline code``` is valid and closed
        tokens = stack.seek_until(lambda tok: tok.type == 'Tick')
        l = len(tokens)
        tokens = tokens[:l-1] # remove the final tick

        self.buffer += '<code class="inline_code">'
        self.buffer += ''.join([t.value for t in tokens])
        self.buffer += '</code>'
        return self.buffer

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

class Plain(State): # root state
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
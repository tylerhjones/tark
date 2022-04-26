from . import State


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
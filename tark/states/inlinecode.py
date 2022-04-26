from . import State


class InlineCode(State):
    def __init__(self):
        self.name = 'InlineCode'
        super().__init__()

    def parse(self, stack):
        tik = stack.pop() # drop first tick
        if tik.value != '`':
            raise Exception('Inline code must start with a tick')
        if stack.peek_type() == 'Tick':
            raise Exception('Inline code must not be empty')
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
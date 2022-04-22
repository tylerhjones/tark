from .structures import Token

class Tokenizer:
    def __init__(self):
        self.tokens: list[Token] = []
        self.digits = [n for n in '0123456789']

    def append(self, chr, type):
        '''Append a token to the token list.
        If the type of the token to append is the same as the last token, 
        append the value to the last token instead of the list.
        '''
        if len(self.tokens) == 0: # first token
            self.tokens.append(Token(type, chr))
            return

        if self.tokens[-1].type == type: # if previous token is same type, append to value
            self.tokens[-1].value += chr
            return

        self.tokens.append(Token(type, chr))

    def scan(self, reader):
        while True:
            c = reader.read(1)
            if c == '': # EOF
                return self.tokens
            if c in self.digits: # number
                self.append(c, 'Digit')
                continue # no idea how to do this in the match statement
            match c:
                case '#': self.append(c, 'Octo')
                case ' ': self.append(c, 'Space')
                case '\n': self.append(c, 'Newline')
                case '`': self.append(c, 'Tick')
                case _: self.append(c, 'Text')

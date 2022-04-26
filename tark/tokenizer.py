from .structures import Token

class Tokenizer:
    def __init__(self):
        self.tokens: list[Token] = []
        self.digits = [n for n in '0123456789']

    def append(self, type, chr):
        '''Append a token to the token list.
        If the type of the token to append is the same as the last token, 
        append the value to the last token instead of the list.
        '''
        if len(self.tokens) > 0:
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
                self.append('Digit',c)
                continue # no idea how to do this in the match statement
            match c:
                case '!': self.append('Bang', c)
                case '#': self.append('Octo',c)
                case ' ': self.append('Space',c)
                case '\n': self.append('Newline',c)
                case '`': self.append('Tick',c)
                case '[': self.append('OpenBracket',c)
                case ']': self.append('CloseBracket',c)
                case '(': self.append('OpenParen',c)
                case ')': self.append('CloseParen',c)
                case '\\': self.append('Escape',c)
                case _: self.append('Text',c)

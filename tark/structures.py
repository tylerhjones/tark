
class Token:
    def __init__(self, type: str, value: str, line=0, row=0):
        self.type = type
        self.value = value
        self.line = line
        self.row = row
        self.length = len(value)

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"

    def __eq__(self, other): # type compare only
        return self.type == other.type

class Stack:
    '''
    Internally a list. This struct provides 'stack' style behavior 
    and some custom functions.
    '''
    stack = []
    row = 0
    line = 0

    def __init__(self, tokens: list[Token]):
        tokens.reverse()
        self.stack = tokens

    def size(self):
        '''Return the size of the stack.'''
        return len(self.stack)
    def push(self, item: Token):
        '''Put item on the stack.'''
        self.stack.append(item)

    def peek(self, n=None):
        '''
        Peek 1 or N tokens from the stack.
        Raise exception if stack is empty.
        '''
        if self.is_empty():
            raise Exception("Attempted to peek at empty stack.")
        if not n:
            return self.stack[-1]
        
        buf = []
        for i in range(1,n+1,1):
            buf.append(self.stack[-i])
        return buf

    def peek_type(self, n=1):
        '''Peek 1 or N of the next token types in the stack.'''
        tokens = self.peek(n)

        for i in range(n):
            tokens[i] = tokens[i].type
        return tokens

    def is_empty(self):
        return len(self.stack) == 0
    def __str__(self):
        return str(self.stack)
    
    def pop(self, n=1):
        buf = []
        for i in range(n):
            self.row += 1
            token = self.stack.pop()
            if token.type == 'Newline':
                self.line += 1
                self.row = 0
            else:
                self.row += token.length
            buf.append(token)

        if n==1:
            return buf[0]
        return buf
    
    def seek_until(self, func)-> list[Token]:
        '''
        From the HEAD of stack, pop until provided lambda(token) is true.
        Return the popped tokens.
        '''
        buffer = []
        while True:
            if self.is_empty(): # exit condition 1
                raise Exception('Stack empty before seek_until found match.')
            token = self.pop()
            buffer.append(token)
            if func(token): # exit condition 2
                return buffer
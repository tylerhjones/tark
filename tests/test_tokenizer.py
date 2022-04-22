from .context import tark
import unittest
from tark.tokenizer import Tokenizer
from tark.structures import Token

class MockReader:
    def __init__(self):
        self.data = ''
    def read(self, n):
        tmp = self.data[:n]
        self.data = self.data[n:]
        return tmp

class TestTokenizer(unittest.TestCase):
    def setUp(self) -> None:
        self.reader = MockReader()
        self.tokenizer = Tokenizer()
    
    def _tokens(self) -> list[Token]:
        return self.tokenizer.scan(self.reader)

    def test_empty_file(self):
        self.reader.data = ''
        self.assertEqual(self._tokens(), [])

    def test_digit(self):
        self.reader.data = '1'
        self.assertEqual(self._tokens(), [Token('Digit', '1')])
    
    def test_multiple_digit(self):
        self.reader.data = '123'
        self.assertEqual(self._tokens(), [Token('Digit', '123')])
    
    def test_space(self):
        self.reader.data = ' '
        self.assertEqual(self._tokens(), [Token('Space', ' ')])
    
    def test_multiple_space(self):
        self.reader.data = '  '
        self.assertEqual(self._tokens(), [Token('Space', '  ')])
    
    def test_octo(self):
        self.reader.data = '#'
        self.assertEqual(self._tokens(), [Token('Octo', '#')])
    
    def test_multiple_octo(self):
        self.reader.data = '##'
        self.assertEqual(self._tokens(), [Token('Octo', '#')])
    
    def test_two_tokens(self):
        self.reader.data = '1A'
        self.assertEqual(self._tokens(), [Token('Digit', '1'), Token('Text', 'A')])
    
    def test_title(self):
        self.reader.data = '# Hello\n\n'
        tokens: list[Token] = self.tokenizer.scan(self.reader)
        self.assertEqual(tokens, 
        [Token('Octo', '#'), Token('Space', ' '), 
            Token('Text', 'Hello'), Token('Newline', '\n\n')])

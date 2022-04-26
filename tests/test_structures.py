from tark.structures import Stack, Token
import unittest

class TestStack(unittest.TestCase):
    def setUp(self) -> None:
        self.stack = Stack([])
    
    def test_empty(self):
        self.assertTrue(self.stack.is_empty())
        self.assertEqual(self.stack.size(), 0)
    
    def test_push_single(self):
        self.stack.push(Token('Digit', '1'))
        self.assertFalse(self.stack.is_empty())
        self.assertEqual(self.stack.size(), 1)
    
    def test_pop_single(self):
        self.stack.push(Token('Digit', '1'))
        self.assertFalse(self.stack.is_empty())

        self.assertEqual(self.stack.pop(), Token('Digit', '1'))
        self.assertEqual(self.stack.size(), 0)

    def test_peek(self):
        self.stack.push(Token('Digit', '1'))
        self.assertEqual(self.stack.peek(), Token('Digit', '1'))
    
    def test_peek_multiple(self):
        self.stack.push(Token('Digit', '1'))
        self.stack.push(Token('Text', 'foo'))
        self.assertEqual(self.stack.peek(n=2), [Token('Text', 'foo'), Token('Digit', '1')])
    
    def test_peek_type(self):
        self.stack.push(Token('Digit', '1'))
        self.stack.push(Token('Text', 'foo'))
        self.assertEqual(self.stack.peek_type(), ['Text'])
    
    def test_peek_type_multiple(self):
        self.stack.push(Token('Digit', '1'))
        self.stack.push(Token('Text', 'foo'))
        self.assertEqual(self.stack.peek_type(n=2), ['Text', 'Digit'])
    
    def test_seek_until(self):
        self.stack.push(Token('Digit', '1'))
        self.stack.push(Token('NewLine', '\n')) # target
        self.stack.push(Token('Digit', '1'))
        self.stack.push(Token('Space', ' '))
        self.stack.push(Token('Digit', '1')) # remember stack order is lifo

        self.assertEqual(self.stack.seek_until(lambda tok: tok.type == 'NewLine'), 
            [Token('Digit', '1'), Token('Space', ' '), 
            Token('Digit', '1'), Token('NewLine', '\n')])
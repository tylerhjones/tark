import unittest

from tark.structures import Stack, Token
from tark.states import *

class TestStates(unittest.TestCase):
    def test_text(self):
        stack = Stack([Token('Text', '<foo!()>')])
        out = Text().parse(stack)
        self.assertEqual(out, '<foo!()>')
        self.assertEqual(stack.size(), 0)
    
    def test_title(self):
        stack = Stack([Token('Octo', '#'), Token('Space', ' '),Token('Text', 'foo'), Token('NewLine', '\n\n')])
        out = Title().parse(stack)
        self.assertEqual(out, '<h1>foo</h1>')
        self.assertEqual(stack.size(), 0)
    
    def test_inline_code(self):
        stack = Stack([Token('Tick', '`'), Token('Text', 'foo'), Token('Tick', '`')])
        out = InlineCode().parse(stack)
        self.assertEqual(out, '<code class="inline_code">foo</code>')
        self.assertEqual(stack.size(), 0)

    def test_code_block(self):
        stack = Stack([
            Token('Tick', '```'),
            Token('Text', 'java'), 
            Token('NewLine', '\n'),
            Token('NewLine', '\n'),
            Token('Text', 'System.out.println("hello tark");'),
            Token('NewLine', '\n'),
            Token('Tick', '```'),
        ])
        out = CodeBlock().parse(stack)
        desire = '<pre class="code_block"><code class="java">\nSystem.out.println("hello tark");\n</code></pre>'
        self.assertEqual(out, desire)
    
    def test_tick(self):
        stack = Stack(
            [Token('Tick', '`'), Token('Text', 'foo'), Token('Tick', '`')])
        Tick().parse(stack) # covered by other states, just checking it doesn't throw

        stack = Stack(
            [Token('Tick', '```'), 
            Token('Text', 'foo'), 
            Token('NewLine','\n'),
            Token('Text', 'bar'),
            Token('Tick', '```')])
        Tick().parse(stack)        
        
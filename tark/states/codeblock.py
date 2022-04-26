from . import State
import string
import re


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
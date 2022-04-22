import sys
from .tokenizer import Tokenizer
from .parser import Parser

def process_file(file_path):
    tokens = None
    tokenizer = Tokenizer()

    with open(file_path, 'r') as f:
        tokens = tokenizer.scan(f) # todo: add timeout

    return Parser().parse(tokens)

if __name__ == '__main__':
    print(process_file(sys.argv[1]))











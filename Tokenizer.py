import re

from Token import Token


class Tokenizer:
    input_string = ''
    tokens_definitions = {
        ('VAR_NAME', r'\@[\w\-]+'),
        ('CONSTANT', r'(?:\#[a-fA-F\0-9]+)|\d*\.?\d+(?:\s*\%|(?:px))?'),
        ('ANCHOR', r'\.[a-zA-Z0-9\-]+'),
        ('STRING', r'[a-zA-Z\-]+'),
        ('SEMICOLON', r'\;'),
        ('COLON', r'\:'),
        ('COMMA', r'\,'),
        ('BRACKET_OP', r'\('),
        ('BRACKET_CLOSE', r'\)'),
        ('BLOCK_OP', r'\{'),
        ('BLOCK_CLOSE', r'\}'),
        ('NEWLINE', r'\n'),
        ('WHITESPACES', r'[\ \t]+'),
        ('COMMENT', r'\/\/.*'),
        ('COMMENT_BLOCK', r'\/\*[\s\S]*?\*\/'),
        ('KEYWORD', r'(?:!important)|(?:all)')
    }
    tokens = []

    def __init__(self, input_content, file=True):
        if file:
            with open(input_content, 'r') as f:
                self.input_string = f.read()
        else:
            self.input_string = input_content

    def tokenize(self):
        for token in self.tokenizer():
            self.tokens.append(token)

    def tokenizer(self):
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in self.tokens_definitions)
        get_token = re.compile(tok_regex).match
        match = get_token(self.input_string)
        line_number = 1
        current_position = 0
        line_start = 0
        while match is not None:
            t = match.lastgroup
            if t == 'NEWLINE':
                line_start = current_position
                line_number += 1
            elif t == 'COMMENT_BLOCK':
                line_number += match.group(t).count('\n')
            elif t != 'WHITESPACES' and t != 'COMMENT':
                yield Token(t, match.group(t), line_number, match.start() - line_start)
            current_position = match.end()
            match = get_token(self.input_string, current_position)
        if current_position != len(self.input_string):
            raise RuntimeError(
                'Error: Unexpected character %r on line %d' % (self.input_string[current_position], line_number)
            )
        yield Token('EOF', '', line_number, current_position - line_start)

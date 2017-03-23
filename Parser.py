from Tokenizer import Tokenizer


class Parser:
    def __init__(self, input_content, file=True, debug=False):
        self.tokenizer = Tokenizer(input_content, file)
        self.tokenizer.tokenize()
        self.token = None
        self.pos = 0
        self.info = []
        self.debug = debug

    def take_token(self, token_type_list, eps=False):
        self.token = self.next_token()
        if self.debug:
            print(self.token)
        if self.token.type not in token_type_list:
            if eps:
                self.token = self.prev_token()
                return 'EPS'
            else:
                self.raise_error(
                    "Unexpected token: %s at '%s' on line %d column %d; Expected one of %s"
                    % (self.token.type, self.token.value, self.token.line, self.token.column, str(token_type_list))
                )
        return self.token

    def take_tokens(self, token_type_list):
        for token_type in token_type_list:
            self.take_token(token_type)

    def prev_token(self):
        self.pos -= 1
        return self.tokenizer.tokens[self.pos - 1]

    def next_token(self):
        self.pos += 1
        return self.tokenizer.tokens[self.pos - 1]

    @staticmethod
    def raise_error(msg='Unexpected error occurred'):
        raise RuntimeError('Parser error; %s' % msg)

    def info_log(self, stmt):
        self.info.append(stmt + ' - OK')
        if self.debug:
            print(self.info[-1])

    def reset(self):
        self.pos = 0
        self.info = []

    def parse(self):
        self.reset()
        self.start()
        return

    def start(self):
        # self.next_token()
        self.x_elems()
        return

    # noinspection SpellCheckingInspection
    def x_elems(self):
        self.take_token(['ANCHOR', 'VAR_NAME', 'EOF'])
        if self.token.type == 'EOF':
            return
        else:
            self.x_elem()
        self.x_elems()

    def x_elem(self):
        if self.token.type == 'ANCHOR':
            self.x_style()
        elif self.token.type == 'VAR_NAME':
            self.x_var_def()
        else:
            self.raise_error()

    def x_style(self):
        self.take_token(['BLOCK_OP'])
        self.x_items()
        self.info_log('style')

    def x_items(self):
        eps = self.take_token(['VAR_NAME', 'STRING', 'ANCHOR', 'BLOCK_CLOSE'], eps=True)
        if eps == 'EPS':
            return
        elif self.token.type == 'VAR_NAME':
            self.x_var_def()
        elif self.token.type == 'STRING':
            self.take_token(['COLON'])
            self.x_value()
            self.x_properties()
            self.take_token(['SEMICOLON'])
        elif self.token.type == 'ANCHOR':
            self.x_style()
        elif self.token.type == 'BLOCK_CLOSE':
            return
        else:
            self.raise_error()
        self.info_log('items')
        self.x_items()

    def x_properties(self):
        # TODO properties
        eps = self.take_token(['CONSTANT', 'STRING', 'VAR_NAME'], True)
        pass

    def x_var_def(self):
        self.take_token(['COLON'])
        self.x_value()
        self.take_token(['SEMICOLON'])
        self.info_log('var_def')

    def x_value(self, eps_mode=False):
        eps = self.take_token(['CONSTANT', 'STRING', 'VAR_NAME'], eps_mode)
        if eps_mode and eps == 'EPS':
            pass
        elif self.token.type == 'CONSTANT':
            pass
        elif self.token.type == 'STRING':
            eps = self.take_token(['BRACKET_OP'], True)
            if eps == 'EPS':
                pass
            else:
                self.x_values()
                self.take_token(['BRACKET_CLOSE'])
        elif self.token.type == 'VAR_NAME':
            pass
        else:
            self.raise_error()

    def x_values(self):
        self.x_value(True)
        eps = self.take_token(['COMMA'], True)
        if eps == 'EPS':
            pass
        else:
            self.x_values()

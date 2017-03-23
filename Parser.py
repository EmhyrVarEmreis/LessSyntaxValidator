from Tokenizer import Tokenizer


class Parser:
    def __init__(self, input_content, file=True, debug=False):
        self.tokenizer = Tokenizer(input_content, file)
        self.tokenizer.tokenize()
        self.token = None
        self.is_debug = debug
        self.pos = 0
        self.info = []
        self.debug = []
        self.eps = False

    def take_token(self, token_type_list, eps=False):
        self.eps = False
        self.token = self.next_token()
        if self.is_debug:
            print(self.token)
        if self.token.type not in token_type_list:
            if eps:
                self.token = self.prev_token()
                self.eps = True
                if self.is_debug:
                    print(self.eps)
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

    def log_info(self, stmt):
        self.info.append(stmt + ' - OK')
        if self.is_debug:
            print(self.info[-1])

    def log_debug(self, stmt):
        self.debug.append(stmt)
        if self.is_debug:
            print(stmt)

    def reset(self):
        self.pos = 0
        self.info = []
        self.debug = []
        self.eps = False

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
        self.log_debug('x_elems')
        self.take_token(['ANCHOR_OP', 'VAR_NAME', 'EOF'])
        if self.token.type == 'EOF':
            return
        else:
            self.x_elem()
        self.x_elems()

    def x_elem(self):
        self.log_debug('x_elem')
        if self.token.type == 'ANCHOR_OP':
            self.x_style()
        elif self.token.type == 'VAR_NAME':
            self.x_var_def()
        else:
            self.raise_error()

    def x_style(self):
        self.log_debug('x_style')
        self.x_items()
        self.log_info('style')

    def x_items(self):
        self.log_debug('x_items')
        eps = self.take_token(['VAR_NAME', 'STRING', 'ANCHOR_OP', 'ANCHOR_CLOSE'], eps=True)
        if eps == 'EPS':
            return
        elif self.token.type == 'VAR_NAME':
            self.x_var_def()
        elif self.token.type == 'STRING':
            self.take_token(['COLON'])
            self.x_value()
            self.x_properties()
            self.take_token(['SEMICOLON'])
        elif self.token.type == 'ANCHOR_OP':
            self.x_style()
        elif self.token.type == 'ANCHOR_CLOSE':
            return
        else:
            self.raise_error()
        self.log_info('items')
        self.x_items()

    def x_properties(self):
        self.log_debug('x_properties')
        self.x_value(True)
        if self.eps:
            return
        else:
            self.x_properties()

    def x_var_def(self):
        self.log_debug('x_var_def')
        self.take_token(['COLON'])
        self.x_value()
        self.take_token(['SEMICOLON'])
        self.log_info('var_def')

    def x_value(self, eps_mode=False):
        self.log_debug('x_value')
        eps = self.take_token(['CONSTANT', 'STRING', 'VAR_NAME', 'FUNCTION_OP'], eps_mode)
        if eps_mode and eps == 'EPS':
            pass
        elif self.token.type == 'CONSTANT':
            pass
        elif self.token.type == 'STRING':
            pass
        elif self.token.type == 'FUNCTION_OP':
            self.x_values()
            self.take_token(['BRACKET_CLOSE'])
        elif self.token.type == 'VAR_NAME':
            pass
        else:
            self.raise_error()

    def x_values(self):
        self.log_debug('x_values')
        self.x_value(True)
        eps = self.take_token(['COMMA'], True)
        if eps == 'EPS':
            pass
        else:
            self.x_values()

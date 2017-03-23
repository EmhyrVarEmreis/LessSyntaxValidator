import collections


# noinspection PyClassHasNoInit
class Token(collections.namedtuple('Token', ['type', 'value', 'line', 'column'])):
    __slots__ = ()

    def __str__(self):
        s = 'Token{type='
        s += self.prepare_string(str(self.type), 16)
        s += ' value='
        s += self.prepare_string(str(self.value), 16)
        s += ' line='
        s += self.prepare_string(str(self.line), 4)
        s += ' column='
        s += '\'' + str(self.column) + '\''
        s += '}'
        return s

    @staticmethod
    def prepare_string(s, max):
        s = s.replace('\n', '\\n').replace('\t', '\\t')
        l = len(s)
        if l > max:
            s = s[0:max - 3] + '...'
        elif l == max:
            s = s
        else:
            s += '\',' + ' ' * (max - l)
            return '\'' + s
        return '\'' + s + '\','

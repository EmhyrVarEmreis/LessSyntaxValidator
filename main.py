from Parser import Parser
from Tokenizer import Tokenizer

file = 'F:\\dev\\private\\github\\LessSyntaxValidator\\test\\t0.less'

print("Tokens:")
t = Tokenizer(file)
t.tokenize()
for tt in t.tokens:
    print('\t' + str(tt))

print("Parse:")
p = Parser(file)
p.parse()
for pp in p.info:
    print('\t' + str(pp))
print('\t\tOK')

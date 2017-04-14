import re

filename = '../test/fsm.def.00.txt'

transitions = {}
regex_set = {}
symbol_start = None
symbol_end = []

with open(filename) as f:
    is_trans = False
    line_num = 0
    regex_list = []
    for line in f:
        line = line.strip()
        if not is_trans and line == '###':
            is_trans = True
        if is_trans:
            t = line.split(' ')
            transitions[t[0]] = {}
            for idx, val in enumerate(t[1:]):
                transitions[t[0]][regex_list[idx]] = val
        else:
            line_num += 1
            if line_num == 1:
                symbol_start = line
            elif line_num == 2:
                symbol_end = line.split(' ')
            else:
                t = line.split(' ', 1)
                regex_set[t[0]] = r'' + t[1]
                regex_list.append(t[0])

regex_set = {k: re.compile(v) for k, v in regex_set.items()}

filename = '../test/fsm.txt'

buffer = ''
current_state = symbol_start

with open(filename) as f:
    is_end = False
    while True:
        c = f.read(1)
        if not c:
            is_end = True
        # print(current_state + ' [' + buffer + ']')
        key = None
        for key_tmp in transitions[current_state].keys():
            match = regex_set[key_tmp].match(c)
            if match is not None:
                key = key_tmp
                break
        if key is None:
            # print(current_state)
            if current_state in symbol_end:
                print(buffer)
            buffer = ''
            current_state = symbol_start
        else:
            # print('\tmatch ' + key)
            buffer += c
            current_state = transitions[current_state][key]
        if is_end:
            break

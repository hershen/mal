

special_charecters = '[]{}()\'`~^@'

class Reader():
    def __init__(self, tokens):
        print('tokens = ', tokens)
        self.tokens = tokens
        self.current_index = 0

    def peek(self):
        return self.tokens[self.current_index]

    def next(self):
        current_value = self.tokens[self.current_index]
        self.current_index += 1

        return current_value

    def empty(self):
        return self.current_index >= len(self.tokens)

def tokenize(line, tokens=[]):
    print(line, tokens)
    line = line.lstrip(' \t\n\r,')

    if len(line) == 0:
        return tokens

    line_len = len(line)

    # ~@
    if line[:2] == '~@':
        return tokenize(line[2:], tokens + ['~@'])

    # Special charecters
    if line[0] in special_charecters:
        return tokenize(line[1:], tokens + [line[0]])
    
    # Comment
    if line[0] == ';':
        return tokenize('', tokens + [line])

    # Double quotes
    if line[0] == '"':
        tmp_start_index = idx + 1
        while True:
            next_double_quote_index = line.find('"', tmp_start_index)
            if next_double_quote_index == -1:
                raise('Found unbalenced double quotes')

            before_double_quotes_index = next_double_quote_index - 1
            if line[before_double_quotes_index] != '\\':
                return tokenize(line[:next_double_quote_index], tokens + [line[idx:next_double_quote_index]])
            else:
                #Found \" - continue searching for closing "
                pass

    # Non-special charecter sequence
    else:
        for char in special_charecters + ' \'",;':
            end_of_sequence_index = line.find(char)
            if end_of_sequence_index >= 0:
                return tokenize(line[end_of_sequence_index:], tokens + [line[:end_of_sequence_index]])
        # line is one long sequence
        return tokenize('', tokens + [line])

def read_form(reader):
    if reader.empty():
        return ''

    next_token = reader.peek()
    
    if next_token[0] == '(':
        return read_list(reader)
    else:
        return read_atom(reader)

def read_list(reader):
    mal_list = [reader.next()] # mal_list should now be ['(']
    while True:
        mal_list.append(read_form(reader))
        if mal_list[-1] == ')':
            break
    return mal_list        

def read_atom(reader):
    token = reader.next()
    if token[0].isdigit():
        return int(token)
    else:
        return token

def read_str(line):
    tokens = tokenize(line)
    reader = Reader(tokens)
    return read_form(reader)



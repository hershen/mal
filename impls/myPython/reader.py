import mal_types

special_charecters = '[]{}()\'`~^@'

class Reader():
    def __init__(self, tokens):
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
        tmp_start_index = 1
        while True:
            next_double_quote_index = line.find('"', tmp_start_index)
            if next_double_quote_index == -1:
                raise ValueError('unbalanced "')

            before_double_quotes_index = next_double_quote_index - 1
            if line[before_double_quotes_index] != '\\':
                return tokenize(line[next_double_quote_index+1:], tokens + [line[:next_double_quote_index+1]])
            else:
                #Found \" - continue searching for closing "
                tmp_start_index = next_double_quote_index + 1

    # Non-special charecter sequence
    else:
        end_sequence_chars_indices = sorted([line.find(char) for char in (special_charecters + ' \'",;') if line.find(char) != -1])

        if not end_sequence_chars_indices: # line is one long sequence
            return tokenize('', tokens + [line])

        first_end_sequence_char_index = end_sequence_chars_indices[0]

        return tokenize(line[first_end_sequence_char_index:], tokens + [line[:first_end_sequence_char_index]])

def read_form(reader):
    if reader.empty():
        return ''

    next_token = reader.peek()
    
    if next_token[0] in '([':
        return read_list(reader)
    else:
        return read_atom(reader)

def read_list(reader):
    mal_list = mal_types.List(reader.next()) # mal_list should now be ['('] or ['[']
    while True:
        mal_object = read_form(reader)
        is_string = isinstance(mal_object, str)

        if is_string and mal_object == '': #reached reader end
            raise ValueError(f'unbalanced "{mal_types.closing_paren_style[mal_list[0]]}"')

        mal_list.append(mal_object)
        if is_string and mal_object in ')]':
            break
    return mal_list        

def read_atom(reader):
    token = reader.next()
    if token[0].isdigit() or (len(token)>2 and token[0] == '-' and token[1].isdigit()):
        return mal_types.Int(token)

    elif token[0] == '"':
        string = token.replace('\\"', '"') \
                      .replace('\\\\', '\\')
        return mal_types.String(string)

    else:
        return token

def read_str(line):
    tokens = tokenize(line)
    reader = Reader(tokens)
    return read_form(reader)



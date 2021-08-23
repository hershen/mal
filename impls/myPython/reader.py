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

def tokenize(line, tokens):
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
        EOF_index = line.find(chr(10))
        if EOF_index == -1: # No end of line, ignore all rest of line
            return tokenize('', tokens + [line])
        else:
            return tokenize(line[EOF_index:], tokens) #ignore current comment

    # Double quotes
    if line[0] == '"':
        tmp_start_index = 1
        while True:
            next_double_quote_index = line.find('"', tmp_start_index)
            if next_double_quote_index == -1:
                raise ValueError('unbalanced "')

            if line[next_double_quote_index - 1] != '\\' or line[next_double_quote_index - 2 : next_double_quote_index] == '\\\\':
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

def remove_new_lines(tokens):
    return [token.rstrip() for token in tokens]

quote_symbol_to_word = {"'":  mal_types.Symbol('quote'),
                        '`':  mal_types.Symbol('quasiquote'),
                        '~':  mal_types.Symbol('unquote'),
                        '~@': mal_types.Symbol('splice-unquote'),
                        '@':  mal_types.Symbol('deref')
                        }

def is_list_type(token):
    return token[0] in mal_types.closing_paren_style.keys()

def read_quote(reader):
    quote_symbol = reader.next()
    return mal_types.List([quote_symbol_to_word[quote_symbol], read_form(reader)])

def read_with_meta(reader):
    carrot_symbol = reader.next()
    first_arg = read_form(reader)
    second_arg = read_form(reader)
    return mal_types.List(['with-meta', second_arg, first_arg])

def read_form(reader):
    """"
    Peek at next token and returns mal_type.
    """

    if reader.empty():
        return mal_types.String('')

    next_token = reader.peek()
    
    if is_list_type(next_token):
        return read_list(reader)
    elif next_token in quote_symbol_to_word.keys():
        return read_quote(reader)
    elif next_token == '^':
        return read_with_meta(reader)
    else:
        return read_atom(reader)

def read_list(reader):
    open_paren = reader.next() # This should be the opening paren type ( [ {

    if open_paren == '(':
        mal_list_variant = mal_types.List()
    elif open_paren == '[':
        mal_list_variant = mal_types.Vector()
    elif open_paren == '{':
        mal_list_variant = mal_types.Hash_map()

    closing_paren = mal_types.closing_paren_style[open_paren]
    while True:
        if reader.empty():
            raise ValueError(f'unbalanced "{mal_list_variant.open_paren}"')

        mal_object = read_form(reader)

        if mal_object == closing_paren:
            break

        mal_list_variant.append(mal_object)

    return mal_list_variant

slash_preceded_charecters = ['\\', '"']

def remove_escape_backslash(input_string):
    output_string = ''
    iterator = iter(input_string)
    for char in iterator:
        if char == '\\':
            next_char = next(iterator, None)
            if next_char in slash_preceded_charecters:
                char = next_char #skip the '\' character
            elif next_char == 'n':
                output_string += chr(10)
                char = next_char = ''
            else: # "undo" advancing the iterator
                output_string += char
                char = next_char

        try:
            output_string += char
        except TypeError: #char is NoneType
            raise ValueError('unbalanced "')

    return ''.join(output_string)


def read_atom(reader):
    """
    Returns mal_type
    """
    token = reader.next()
    if token[0].isdigit() or (len(token)>1 and token[0] == '-' and token[1].isdigit()):
        return mal_types.Int(token)

    elif token[0] == '"':
        return mal_types.String(remove_escape_backslash(token[1:-1]))
    
    elif token[0] == ':':
        return mal_types.Keyword(token)
    
    elif token == 'nil':
        return mal_types.Nil()

    elif token == 'true':
        return mal_types.true()
    
    elif token == 'false':
        return mal_types.false()

    else:
        return mal_types.Symbol(token)

def read_str(line):
    tokens = tokenize(line, [])
    tokens = remove_new_lines(tokens)
    reader = Reader(tokens)
    return read_form(reader)



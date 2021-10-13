from mal_python import mal_types

special_charecters = "[]{}()'`~^@"


class PeakableIterator:
    """Class to iterate through tokens"""

    def __init__(self, elements):
        self.elements = elements
        self.current_index = 0

    def peek(self):
        """Return current token, without advancing to the next token"""
        return self.elements[self.current_index]

    def next(self):
        """Return current token, and advance to the next token"""
        current_value = self.elements[self.current_index]
        self.current_index += 1

        return current_value

    def empty(self):
        return self.current_index >= len(self.elements)


def remove_white_spaces(line):
    return line.lstrip(" \t\n\r,")


def tokenize(line):
    """parse a line of text into a list of mal tokens"""

    tokens = []

    line = remove_white_spaces(line)

    while line:

        # ~@
        if line[:2] == "~@":
            tokens.append("~@")
            line = line[2:]

        # Special characters
        elif line[0] in special_charecters:
            tokens.append(line[0])
            line = line[1:]

        # Comment
        elif line[0] == ";":
            EOF_index = line.find(chr(10))
            if EOF_index == -1:  # No end of line, ignore all rest of line
                line = ""
            else:
                line = line[EOF_index:]  # ignore current comment

        # Double quotes
        elif line[0] == '"':
            tmp_start_index = 1
            while True:
                next_double_quote_index = line.find('"', tmp_start_index)
                if next_double_quote_index == -1:
                    raise ValueError('unbalanced "')

                if (
                    line[next_double_quote_index - 1] != "\\"
                    or line[next_double_quote_index - 2 : next_double_quote_index]
                    == "\\\\"
                ):  # Found closing "
                    tokens.append(line[: next_double_quote_index + 1])
                    line = line[next_double_quote_index + 1 :]
                    break
                else:
                    # Found \" - continue searching for closing "
                    tmp_start_index = next_double_quote_index + 1

        # Non-special character sequence
        else:
            end_sequence_chars_indices = sorted(
                [
                    line.find(char)
                    for char in (special_charecters + " '\",;")
                    if line.find(char) != -1
                ]
            )

            if not end_sequence_chars_indices:  # line is one long sequence
                tokens.append(line)
                line = ""

            else:
                first_end_sequence_char_index = end_sequence_chars_indices[0]
                tokens.append(line[:first_end_sequence_char_index])
                line = line[first_end_sequence_char_index:]

        line = remove_white_spaces(line)

    return tokens


def remove_new_lines(tokens):
    return [token.rstrip() for token in tokens]


quote_symbol_to_word = {
    "'": mal_types.Symbol("quote"),
    "`": mal_types.Symbol("quasiquote"),
    "~": mal_types.Symbol("unquote"),
    "~@": mal_types.Symbol("splice-unquote"),
    "@": mal_types.Symbol("deref"),
}


def is_list_type(token):
    return token[0] in mal_types.closing_paren_style.keys()


def parse_quote(peakable_iterator):
    quote_symbol = peakable_iterator.next()
    return mal_types.List(
        [quote_symbol_to_word[quote_symbol], parse_tokens(peakable_iterator)]
    )


def parse_with_meta(peakable_iterator):
    _ = peakable_iterator.next()  # This is the carrot symbol
    first_arg = parse_tokens(peakable_iterator)
    second_arg = parse_tokens(peakable_iterator)
    return mal_types.List([mal_types.Symbol("with-meta"), second_arg, first_arg])


def parse_list(peakable_iterator):
    open_paren = peakable_iterator.next()  # This should be the opening paren type ( [ {

    if open_paren == mal_types.List.open_paren:
        mal_list_variant = mal_types.List()
    elif open_paren == mal_types.Vector.open_paren:
        mal_list_variant = mal_types.Vector()
    elif open_paren == mal_types.HashMap.open_paren:
        mal_list_variant = mal_types.HashMap()
    else:
        raise ValueError(f"Unrecognized open paren {open_paren}")

    while True:
        if peakable_iterator.empty():
            raise ValueError(f'unbalanced "{mal_list_variant.open_paren}"')

        mal_object = parse_tokens(peakable_iterator)

        if mal_object == mal_list_variant.close_paren:
            break

        mal_list_variant.append(mal_object)

    return mal_list_variant


def isNumber(string):
    return string[0].isdigit() or (
        len(string) > 1 and string[0] == "-" and string[1].isdigit()
    )


slash_preceded_charecters = ["\\", '"']


def remove_escape_backslash(input_string):
    output_string = ""
    iterator = iter(input_string)
    for char in iterator:
        if char == "\\":
            next_char = next(iterator, None)
            if next_char in slash_preceded_charecters:
                char = next_char  # skip the '\' character
            elif next_char == "n":
                output_string += chr(10)
                char = next_char = ""
            else:  # "undo" advancing the iterator
                output_string += char
                char = next_char

        try:
            output_string += char
        except TypeError:  # char is NoneType
            raise ValueError('unbalanced "')

    return "".join(output_string)


def parse_single_token(peakable_iterator):
    """Returns mal type"""

    token = peakable_iterator.next()
    if isNumber(token):
        return mal_types.Int(token)

    elif token[0] == '"':
        return mal_types.String(remove_escape_backslash(token[1:-1]))

    elif token[0] == ":":
        return mal_types.Keyword(token)

    elif token == "nil":
        return mal_types.Nil()

    elif token == "true":
        return mal_types.TrueType()

    elif token == "false":
        return mal_types.FalseType()

    else:
        return mal_types.Symbol(token)


def parse_tokens(peakable_iterator):
    """Peek at next token and parse with the appropriate function"""

    if peakable_iterator.empty():
        return mal_types.String("")

    next_token = peakable_iterator.peek()

    if is_list_type(next_token):
        return parse_list(peakable_iterator)
    elif next_token in quote_symbol_to_word.keys():
        return parse_quote(peakable_iterator)
    elif next_token == "^":
        return parse_with_meta(peakable_iterator)
    else:
        return parse_single_token(peakable_iterator)


def parse_string(line):
    tokens = tokenize(line)
    tokens = remove_new_lines(tokens)
    peakable_iterator = PeakableIterator(tokens)
    return parse_tokens(peakable_iterator)

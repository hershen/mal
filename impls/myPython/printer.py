import mal_types
import reader

def add_escape_backslash(input_string):
    input_string_with_escape_chars = ['\\' + char if char in reader.slash_preceded_charecters else char for char in input_string[1:-1]]
    return '"' + input_string_with_escape_chars + '"'

def pr_str(mal_type, print_readably):
    string_representation = str(mal_type)

    # print(' before = ', string_representation, type(mal_type))
    if print_readably and isinstance(mal_type, mal_types.String):
        string_representation = '"' + string_representation[1:-1].replace('\\', '\\\\') \
                                                                 .replace('"', '\\"') \
                                                                 .replace('\\\\n', '\\n') \
                              + '"'
    # print(' after = ', string_representation)

    return string_representation

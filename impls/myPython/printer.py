import mal_types
import reader

def add_escape_backslash(input_string):
    input_string_with_escape_chars = ''.join(['\\' + char if char in reader.slash_preceded_charecters else char for char in input_string])
    return mal_types.String(input_string_with_escape_chars.replace(chr(10), '\\n'))

def pr_str(mal_type, print_readably):
    if callable(mal_type):
        return '#<function>'

    if isinstance(mal_type, mal_types.String) and print_readably:
        return add_escape_backslash(mal_type)

    return mal_type

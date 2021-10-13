from mal_python import mal_types
from mal_python import parser


def add_escape_backslash(input_string):
    input_string_with_escape_chars = "".join(
        [
            "\\" + char if char in parser.slash_preceded_charecters else char
            for char in input_string
        ]
    )
    return mal_types.String(input_string_with_escape_chars.replace(chr(10), "\\n"))


def print_string(mal_type, print_readably):
    if callable(mal_type):
        return "#<function>"

    if isinstance(mal_type, mal_types.String) and print_readably:
        return '"' + str(add_escape_backslash(mal_type)) + '"'

    elif isinstance(mal_type, mal_types.ListVariant):
        return (
            mal_type.open_paren
            + " ".join(print_string(item, print_readably) for item in mal_type)
            + mal_type.close_paren
        )

    return str(mal_type)

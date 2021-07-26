import mal_types

def pr_str(mal_type, print_readably):
    string_representation = str(mal_type)

    # print(' before = ', string_representation, type(mal_type))
    if print_readably and isinstance(mal_type, mal_types.String):
        string_representation = '"' + string_representation[1:-1].replace('\\', '\\\\') \
                                                                 .replace('"', '\\"')   \
                                                                 .replace('{', '\\{')   \
                                                                 .replace('}', '\\}')   \
                              + '"'
            #                                                  .replace(')', '\\)')   \
            #                                                  .replace('"', '\\"')   
    # print(' after = ', string_representation)

    return string_representation

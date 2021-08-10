#!/usr/bin/python3

import operator

import mal_types
import reader
import printer

repl_env = {'+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv
            }

class UnrecognizedSymbol(Exception):
    pass

def eval_ast(mal_type, environment):
    if isinstance(mal_type, mal_types.Symbol):
        try:
            return repl_env[mal_type]
        except KeyError:
            raise UnrecognizedSymbol(f'Unrecognized symbol {mal_type}')

    if isinstance(mal_type, mal_types.List):
        return mal_types.List([EVAL(item) for item in mal_type])

    if isinstance(mal_type, mal_types.Vector):
        return mal_types.Vector([EVAL(item) for item in mal_type])

    if isinstance(mal_type, mal_types.Hash_map):
        eval_only_values = lambda index, item: item if index%2 == 0 else EVAL(item)
        return mal_types.Hash_map([ eval_only_values(index, item) for index, item in enumerate(mal_type)])

    return mal_type

def READ(line):
    return reader.read_str(str(line))

def EVAL(mal_type, environment=repl_env):
    if not isinstance(mal_type, mal_types.List):
        return eval_ast(mal_type, environment)
    
    #mal_type is List
    if len(mal_type):
        evaluated_list = eval_ast(mal_type, environment)
        return evaluated_list[0](*evaluated_list[1:])

    #mal_type is empty List
    return mal_type

def PRINT(mal_type):
    return printer.pr_str(mal_type, print_readably=True)

def rep(line):
    read = READ(line)
    evaluated = EVAL(read, repl_env)
    printed = PRINT(evaluated)
    return printed

if __name__ == "__main__":
    while True:
        try: 
            line = input('user> ')
            print(rep(line))
        except ValueError as e:
            print(e)
        except UnrecognizedSymbol as e:
            print(e)
        except EOFError:
            #EOF
            break


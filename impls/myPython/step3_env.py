#!/usr/bin/python3

import operator

import env
import mal_types
import reader
import printer


repl_env = env.Env('nil')
repl_env.set(mal_types.Symbol('+'), operator.add)
repl_env.set(mal_types.Symbol('-'), operator.sub)
repl_env.set(mal_types.Symbol('*'), operator.mul)
repl_env.set(mal_types.Symbol('/'), operator.truediv)

class UnrecognizedSymbol(Exception):
    pass

class UnrecognizedSymbol(Exception):
    pass

def eval_ast(mal_type, environment):
    if isinstance(mal_type, mal_types.Symbol):
        try:
            return environment.get(mal_type)
        except KeyError:
            raise UnrecognizedSymbol(f'Unrecognized symbol {mal_type}')

    if isinstance(mal_type, mal_types.List):
        return mal_types.List([EVAL(item, environment) for item in mal_type])

    if isinstance(mal_type, mal_types.Vector):
        return mal_types.Vector([EVAL(item, environment) for item in mal_type])

    if isinstance(mal_type, mal_types.Hash_map):
        eval_only_values = lambda index, item: item if index%2 == 0 else EVAL(item, environment)
        return mal_types.Hash_map([ eval_only_values(index, item) for index, item in enumerate(mal_type)])

    return mal_type

def READ(line):
    return reader.read_str(str(line))

def EVAL(mal_type, environment):
    if not isinstance(mal_type, mal_types.List):
        return eval_ast(mal_type, environment)
    
    #mal_type is List
    if len(mal_type):
        if mal_type[0] == 'def!':
            key = mal_type[1]
            value = EVAL(mal_type[2], environment)
            environment.set(key, value)
            return value

        elif mal_type[0] == 'let*':
            let_environment = env.Env(outer=environment)
            binding_list = mal_type[1]
            
            for key, unevaluated_value in zip(binding_list[::2], binding_list[1::2]):
                let_environment.set(key, EVAL(unevaluated_value, let_environment))

            expression = mal_type[2]
            return EVAL(expression, let_environment)
        else: # "regular" list
            evaluated_list = eval_ast(mal_type, environment)
            function = evaluated_list[0]
            operands = evaluated_list[1:]
            return function(*operands)

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
        except env.MissingKeyInEnvironment as e:
            print(e)
        except EOFError:
            #EOF
            break


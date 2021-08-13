#!/usr/bin/python3

import env
import mal_types
import core
import reader
import printer


repl_env = env.Env(mal_types.Nil())
for key,value in core.ns.items():
    repl_env.set(key, value)

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
    
    if len(mal_type): #mal_type is non-empty List
        operation_type = mal_type[0]
        if operation_type == 'def!':
            key = mal_type[1]
            value = EVAL(mal_type[2], environment)
            environment.set(key, value)
            return value

        elif operation_type == 'let*':
            let_environment = env.Env(outer=environment)
            binding_list = mal_type[1]
            
            for key, unevaluated_value in zip(binding_list[::2], binding_list[1::2]):
                let_environment.set(key, EVAL(unevaluated_value, let_environment))

            expression = mal_type[2]
            return EVAL(expression, let_environment)
        elif operation_type == 'do':
            evaluated_list = eval_ast(mal_type[1:], environment)
            return evaluated_list[-1]
        elif operation_type == 'if':
            condition = EVAL(mal_type[1], environment)
            if isinstance(condition, mal_types.Nil) or isinstance(condition, mal_types.false):
                try:
                    expression_if_false = mal_type[3]
                except IndexError: # No false expression provided
                    return mal_types.Nil()
                return EVAL(expression_if_false, environment)
            else:
                expression_if_true = mal_type[2]
                return EVAL(expression_if_true, environment)

        elif operation_type == 'fn*':
            def closure(*args):
                binds = mal_type[1]
                exprs = mal_types.List([*args])
                new_environment = env.Env(environment, binds, exprs)
                function_body = mal_type[2]
                return EVAL(function_body, new_environment)
            return closure

        else: # "regular" list
            evaluated_list = eval_ast(mal_type, environment)
            function = evaluated_list[0]
            operands = evaluated_list.list[1:]
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
    #Define not symbol
    rep("(def! not (fn* (a) (if a false true)))")
    while True:
        try: 
            line = input('user> ')
            rep_line = rep(line)
            print(str(rep_line))
        except ValueError as e:
            print(e)
        except UnrecognizedSymbol as e:
            print(e)
        except env.MissingKeyInEnvironment as e:
            print(e)
        except EOFError:
            #EOF
            break
        except KeyboardInterrupt: #Ctrl-C
            break


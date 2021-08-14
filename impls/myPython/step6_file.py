#!/usr/bin/python3

import env
import mal_types
import core
import reader
import printer


repl_env = env.Env(mal_types.Nil())
for key,value in core.ns.items():
    repl_env.set(key, value)

#eval functionality
def mal_eval(mal_type):
    return EVAL(mal_type, repl_env)
repl_env.set('eval', mal_eval)

class UnrecognizedSymbol(Exception):
    pass

class UnrecognizedSymbol(Exception):
    pass

class FnState:
    def __init__(self, mal_type, params, env, fn):
        self.mal_type = mal_type
        self.params = params
        self.env = env
        self.fn = fn

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
    while True:
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

                #Tail call optimization - instead of return EVAL(expression, let_environment)
                environment = let_environment
                expression = mal_type[2]
                mal_type = expression

            elif operation_type == 'do':
                evaluated_list = eval_ast(mal_type[1:-1], environment)
                mal_type = mal_type[-1]

            elif operation_type == 'if':
                condition = EVAL(mal_type[1], environment)
                if isinstance(condition, mal_types.Nil) or isinstance(condition, mal_types.false):
                    try:
                        mal_type = mal_type[3]
                    except IndexError: # No false expression provided
                        return mal_types.Nil()
                else:
                    mal_type = mal_type[2]

            elif operation_type == 'fn*':
                def closure(*args):
                    binds = mal_type[1]
                    exprs = mal_types.List([*args])
                    new_environment = env.Env(environment, binds, exprs)
                    function_body = mal_type[2]
                    return EVAL(function_body, new_environment)
                params = mal_type[1]
                body = mal_type[2]
                fn = closure
                return FnState(body, params, environment, fn)

            else: # "regular" list
                evaluated_list = eval_ast(mal_type, environment)
                function = evaluated_list[0]
                operands = evaluated_list[1:]

                if isinstance(function, FnState):
                    mal_type = function.mal_type
                    environment = env.Env(outer = function.env, binds = function.params, exprs = operands)
                else:
                    return function(*operands)

        else: #mal_type is empty List
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

    #Define load-file
    rep('(def! load-file (fn* (f) (eval (read-string (str "(do " (slurp f) "\nnil)")))))')

    while True:
        try: 
            line = input('user> ')
            rep_line = rep(line)
            print(repr(rep_line))
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


#!/usr/bin/python3

import copy
import os
import readline
import sys

import env
import mal_types
import core
import reader
import printer

history_filename = os.path.join(os.path.dirname(__file__), ".history")
history_size = 1000
if not os.path.exists(history_filename):
    open(history_filename, "a").close()

readline.read_history_file(history_filename)
readline.set_history_length(history_size)


class UnrecognizedSymbol(Exception):
    pass


repl_env = env.Env(mal_types.Nil())


def eval_ast(mal_type, environment):
    """
    Evaluate each element of the ast (mal_type).
    If it's a List type, evaluate each element of the list.
    """
    if isinstance(mal_type, mal_types.Symbol):
        try:
            return environment.get(mal_type)
        except KeyError:
            raise UnrecognizedSymbol(f"Unrecognized symbol {mal_type}")

    if isinstance(mal_type, mal_types.List):
        return mal_types.List([EVAL(item, environment) for item in mal_type])

    if isinstance(mal_type, mal_types.Vector):
        return mal_types.Vector([EVAL(item, environment) for item in mal_type])

    if isinstance(mal_type, mal_types.Hash_map):
        eval_only_values = (
            lambda index, item: item if index % 2 == 0 else EVAL(item, environment)
        )
        return mal_types.Hash_map(
            [eval_only_values(index, item) for index, item in enumerate(mal_type)]
        )

    return mal_type


def READ(line):
    return reader.read_str(str(line))


def is_macro_call(mal_type, environment):
    if isinstance(mal_type, mal_types.List) and isinstance(
        mal_type[0], mal_types.Symbol
    ):
        try:
            function = environment.get(mal_type[0])
        except env.MissingKeyInEnvironment:
            return mal_types.false()

        if isinstance(function, mal_types.FunctionState) and function.is_macro:
            return mal_types.true()

    return mal_types.false()


def macroexpand(mal_type, environment):
    while is_macro_call(mal_type, environment):
        function = environment.get(mal_type[0])
        args = mal_type[1:]
        mal_type = function(*args)

    return mal_type


def EVAL(mal_type, environment):
    while True:
        if not isinstance(mal_type, mal_types.List):
            return eval_ast(mal_type, environment)

        if len(mal_type):  # mal_type is non-empty List

            mal_type = macroexpand(mal_type, environment)
            # Ensure result is still List
            if not isinstance(mal_type, mal_types.List):
                return eval_ast(mal_type, environment)

            operation_type = mal_type[0]

            if operation_type == "try*":
                try:
                    return EVAL(mal_type[1], environment)
                except Exception as exception:
                    try:
                        catch_block = mal_type[2]
                    except IndexError:
                        raise env.MissingKeyInEnvironment(f"{mal_type[1]} not found")

                    bind = catch_block[1]
                    exception_value = (
                        exception.value
                        if isinstance(exception, mal_types.MalException)
                        else mal_types.String(str(exception))
                    )
                    new_environment = env.Env(
                        outer=environment, binds=[bind], exprs=[exception_value]
                    )

                    new_eval = catch_block[2]
                    return EVAL(new_eval, new_environment)

            if operation_type == "def!":
                key = mal_type[1]
                value = EVAL(mal_type[2], environment)
                environment.set(key, value)
                return value

            if operation_type == "defmacro!":
                key = mal_type[1]
                function = EVAL(mal_type[2], environment)
                function = copy.deepcopy(function)  # do not mutate orignal function
                function.is_macro = mal_types.true()
                environment.set(key, function)
                return function

            elif operation_type == "let*":
                let_environment = env.Env(outer=environment)
                binding_list = mal_type[1]

                for key, unevaluated_value in zip(
                    binding_list[::2], binding_list[1::2]
                ):
                    let_environment.set(key, EVAL(unevaluated_value, let_environment))

                # Tail call optimization - instead of return EVAL(expression, let_environment)
                environment = let_environment
                expression = mal_type[2]
                mal_type = expression

            elif operation_type == "do":
                evaluated_list = eval_ast(mal_type[1:-1], environment)
                mal_type = mal_type[-1]

            elif operation_type == "if":
                condition = EVAL(mal_type[1], environment)
                if isinstance(condition, mal_types.Nil) or isinstance(
                    condition, mal_types.false
                ):
                    try:
                        mal_type = mal_type[3]
                    except IndexError:  # No false expression provided
                        return mal_types.Nil()
                else:
                    mal_type = mal_type[2]

            elif operation_type == "fn*":

                def closure(*args):
                    binds = mal_type[1]
                    exprs = mal_types.List([*args])
                    new_environment = env.Env(environment, binds, exprs)
                    function_body = mal_type[2]
                    return EVAL(function_body, new_environment)

                params = mal_type[1]
                body = mal_type[2]
                fn = closure
                return mal_types.FunctionState(body, params, environment, fn)

            elif operation_type == "quote":
                return mal_type[1]

            elif (
                operation_type == "quasiquoteexpand"
            ):  # Supposed to be used for debugging - in practice used to pass all tests
                return core.quasiquote(mal_type[1])

            elif operation_type == "quasiquote":
                quasiquote_returned = core.quasiquote(mal_type[1])
                mal_type = quasiquote_returned  # evaluate value returned by quasiquote by tail call optimation in next while iteration

            elif operation_type == "macroexpand":
                return macroexpand(mal_type[1], environment)

            else:  # "regular" list
                evaluated_list = eval_ast(mal_type, environment)
                function = evaluated_list[0]
                operands = evaluated_list[1:]

                if isinstance(function, mal_types.FunctionState):
                    mal_type = function.mal_type
                    environment = env.Env(
                        outer=function.env, binds=function.params, exprs=operands
                    )
                else:
                    return function(*operands)

        else:  # mal_type is empty List
            return mal_type


def PRINT(mal_type):
    return printer.pr_str(mal_type, print_readably=True)


def rep(line):
    read = READ(line)
    evaluated = EVAL(read, repl_env)
    printed = PRINT(evaluated)
    return printed


def set_argv():
    """
    Add command line arguments. If none are given, add empty list
    """
    try:
        args = mal_types.List([mal_types.String(arg) for arg in sys.argv[2:]])
    except IndexError:
        args = mal_types.List([])

    repl_env.set("*ARGV*", args)


def define_new_forms():
    # Define not symbol
    rep("(def! not (fn* (a) (if a false true)))")

    # Define load-file
    rep(
        '(def! load-file (fn* (f) (eval (read-string (str "(do " (slurp f) "\nnil)")))))'
    )

    # eval functionality
    def mal_eval(mal_type):
        return EVAL(mal_type, repl_env)

    repl_env.set("eval", mal_eval)

    rep(
        "(defmacro! cond (fn* (& xs) (if (> (count xs) 0) (list 'if (first xs) (if (> (count xs) 1) (nth xs 1) (throw \"odd number of forms to cond\")) (cons 'cond (rest (rest xs)))))))"
    )

    # host langauge
    rep('(def! *host-language* "python3")')


def print_startup_header():
    rep('(println (str "Mal [" *host-language* "]"))')


if __name__ == "__main__":

    define_new_forms()
    set_argv()

    for key, value in core.ns.items():
        repl_env.set(key, value)

    if len(sys.argv) > 1:
        filename = sys.argv[1]
        rep(f'(load-file "{filename}")')
        exit()

    print_startup_header()

    while True:
        try:
            line = input("user> ")
            rep_line = rep(line)
            print(rep_line)
        except ValueError as e:
            print(e)
        except UnrecognizedSymbol as e:
            print(e)
        except env.MissingKeyInEnvironment as e:
            print(e)
        except EOFError:
            # EOF
            print()
            break
        except KeyboardInterrupt:  # Ctrl-C
            print()
        except FileNotFoundError as e:
            print(e)
        except core.IndexOutOfBounds as e:
            print(e)
        except mal_types.MalException as e:
            print(e)

        readline.write_history_file(history_filename)

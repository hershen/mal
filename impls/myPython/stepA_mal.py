#!/usr/bin/python3

import os
import readline
import sys

from mal_python import core
from mal_python import env
from mal_python import evaluator
from mal_python import mal_types
from mal_python import printer
from mal_python import parser

history_size = 1000
history_directory = os.path.join(os.path.expanduser("~"), ".mal")
history_filename = ".history"


class CommandHistory:
    """Set up command history, even between mal invocations"""

    def __init__(self):
        os.makedirs(history_directory, exist_ok=True)
        self.history_filename = os.path.join(history_directory, history_filename)

        if not os.path.exists(self.history_filename):
            open(self.history_filename, "a").close()

    def open_history_file(self):
        readline.read_history_file(self.history_filename)
        readline.set_history_length(history_size)

    def save_history_file(self):
        readline.write_history_file(self.history_filename)


repl_environment = env.Env(mal_types.Nil())


def READ(line):
    return parser.parse_string(str(line))


def PRINT(mal_type):
    return printer.print_string(mal_type, print_readably=True)


def read_eval_print(line):
    read = READ(line)
    evaluated = evaluator.Evaluator(read, repl_environment).EVAL()
    printed = PRINT(evaluated)
    return printed


def set_argv():
    """Add command line arguments. If none are given, add empty list"""
    try:
        args = mal_types.List([mal_types.String(arg) for arg in sys.argv[2:]])
    except IndexError:
        args = mal_types.List([])

    repl_environment.set("*ARGV*", args)


def load_core_forms():
    for key, value in core.namespace.items():
        repl_environment.set(key, value)


def define_new_forms():
    read_eval_print("(def! not (fn* (a) (if a false true)))")

    read_eval_print(
        '(def! load-file (fn* (f) (eval (read-string (str "(do " (slurp f) "\nnil)")))))'
    )

    def mal_eval(mal_type):
        return evaluator.Evaluator(mal_type, repl_environment).EVAL()

    repl_environment.set("eval", mal_eval)

    read_eval_print(
        "(defmacro! cond (fn* (& xs) (if (> (count xs) 0) (list 'if (first xs) (if (> (count xs) 1) (nth xs 1) (throw \"odd number of forms to cond\")) (cons 'cond (rest (rest xs)))))))"
    )

    read_eval_print('(def! *host-language* "python3")')

    load_core_forms()


def print_startup_header():
    read_eval_print('(println (str "Mal [" *host-language* "]"))')


def repl_loop():
    while True:
        try:
            line = input("user> ")
            evaluated_line = read_eval_print(line)
            print(evaluated_line)
        except (
            ValueError,
            mal_types.UnrecognizedSymbol,
            env.MissingKeyInEnvironment,
            FileNotFoundError,
            core.IndexOutOfBounds,
            mal_types.MalException,
        ) as e:
            print(e)
        except KeyboardInterrupt:  # Ctrl-C
            print()
        except EOFError:
            print()
            return


def main():
    command_history = CommandHistory()
    command_history.open_history_file()

    define_new_forms()
    set_argv()

    if len(sys.argv) > 1:
        filename = sys.argv[1]
        read_eval_print(f'(load-file "{filename}")')
        exit()

    print_startup_header()

    repl_loop()

    command_history.save_history_file()


if __name__ == "__main__":
    main()

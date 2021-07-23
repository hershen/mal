#!/usr/bin/python3

import reader
import printer

def READ(line):
    return reader.read_str(str(line))

def EVAL(mal_type):
    return mal_type

def PRINT(mal_type):
    return printer.pr_str(mal_type)

def rep(line):
    return PRINT(EVAL(READ(line)))

if __name__ == "__main__":
    while True:
        try: 
            line = input('user> ')
        except EOFError:
            print('EOFError')
            break

        print(rep(line))


#!/usr/bin/python3

def READ(line):
    return line

def EVAL(string):
    return string

def PRINT(string):
    return string

def rep(line):
    return PRINT(EVAL(READ(line)))

if __name__ == "__main__":
    while True:
        try: 
            line = input('user> ')
        except EOFError:
            break

        print(rep(line))


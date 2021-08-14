import operator

import mal_types
import printer
import reader

def prn(*x):
    try:
        print(printer.pr_str(x[0], print_readably=True))
    except IndexError:
        pass
    return 'nil'

def true_false(x):
    return mal_types.true() if x else mal_types.false()

def prstr(*items):
    items = [mal_types.String('"' + str(item) + '"') for item in items if isinstance(item, mal_types.String)]
    joined_string = ' '.join([str(printer.pr_str(item, print_readably=True)) for item in items])
    return mal_types.String(joined_string)

def str_function(*items):
    joined_string = ''.join([str(printer.pr_str(item, print_readably=False)) for item in items])
    return mal_types.String(joined_string)

def prn(*items):
    joined_string = ' '.join([str(printer.pr_str(item, print_readably=True)) for item in items])
    print(joined_string)
    return mal_types.Nil()

def println(*items):
    joined_string = ' '.join([str(printer.pr_str(item, print_readably=False)) for item in items])
    print(joined_string)
    return mal_types.Nil()

def slurp(string):
    with open(str(string), 'r') as f:
        return mal_types.String(f.read())

ns = {mal_types.Symbol('+'): operator.add,
      mal_types.Symbol('-'): operator.sub,
      mal_types.Symbol('*'): operator.mul,
      mal_types.Symbol('/'): operator.truediv,
      
      mal_types.Symbol('prn'):  lambda *x: prn(*x),
      mal_types.Symbol('list'): lambda *x: mal_types.List(x),
      mal_types.Symbol('list?'): lambda *x: true_false(isinstance(x[0], mal_types.List)),
      mal_types.Symbol('empty?'): lambda *x: true_false(len(x[0]) == 0),
      mal_types.Symbol('count'): lambda *x: len(x[0]),
      mal_types.Symbol('='):  lambda *x: true_false(x[0] == x[1]),
      mal_types.Symbol('<'):  lambda *x: true_false(x[0] <  x[1]),
      mal_types.Symbol('<='): lambda *x: true_false(x[0] <= x[1]),
      mal_types.Symbol('>'):  lambda *x: true_false(x[0] >  x[1]),
      mal_types.Symbol('>='): lambda *x: true_false(x[0] >= x[1]),

      mal_types.Symbol('pr-str'): lambda *x: prstr(*x),
      mal_types.Symbol('str'): lambda *x: str_function(*x),
      mal_types.Symbol('prn'): lambda *x: prn(*x),
      mal_types.Symbol('println'): lambda *x: println(*x),
    
      mal_types.Symbol('read-string'): lambda x: reader.read_str(str(x)),
      mal_types.Symbol('slurp'): lambda x: slurp(x)
      }

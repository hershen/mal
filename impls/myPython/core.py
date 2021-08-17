import operator

import mal_types
import printer
import reader

class IndexOutOfBounds(Exception):
    pass

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
    try:
        with open(str(string), 'r') as f:
            return mal_types.String(f.read())
    except FileNotFoundError:
        error_string = f'Could not open file {string}'
        raise FileNotFoundError(error_string)

def reset(atom, mal_value):
    atom.set(mal_value)
    return mal_value

def swap(atom, function, *args):
    atom.set(function(atom.get(), *args))
    return atom.get()

def concat(*lists):
    new_list = []
    for l in lists:
        new_list.extend(l)
    return mal_types.List(new_list)

def quasiquote(mal_type, ignore_unquote=False):
    if isinstance(mal_type, mal_types.List):
        try:
            if len(mal_type) > 1 and mal_type[0] == 'unquote' and not ignore_unquote:
                return mal_type[1]
        except IndexError:
            raise ValueError(f'Cannot quasiquote on List {mal_type}')

        if len(mal_type)==0:
            return mal_type
        if isinstance(mal_type[0], mal_types.List) and len(mal_type[0])>1 and mal_type[0][0] == 'splice-unquote':
            first_element_of_splice = mal_type[0][1]
            return mal_types.List([mal_types.Symbol('concat'), first_element_of_splice, quasiquote(mal_type[1:])])
        return mal_types.List([mal_types.Symbol('cons'), quasiquote(mal_type[0]), quasiquote(mal_type[1:])])

    if isinstance(mal_type, mal_types.Vector):
        new_list = mal_types.List(mal_type.list)
        return mal_types.List([mal_types.Symbol('vec'), quasiquote(new_list, ignore_unquote=True)])

    if isinstance(mal_type, mal_types.Symbol) or isinstance(mal_type, mal_types.Hash_map):
        return mal_types.List([mal_types.Symbol('quote'), mal_type])
    return mal_type

def nth(list_type, index):
    try:
        return list_type[index]
    except IndexError:
        raise IndexOutOfBounds(f'List type {list_type} does not have an element at index {index}')

def first(list_type):
    try:
        return list_type[0]
    except IndexError:
        return mal_types.Nil()
    except TypeError:
        return mal_types.Nil()

def rest(list_type):
    try:
        return mal_types.List(list_type[1:])
    except IndexError:
        return mal_types.List()
    except TypeError:
        return mal_types.List()

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
      mal_types.Symbol('slurp'): lambda x: slurp(x),

      mal_types.Symbol('atom'): lambda x: mal_types.Atom(x),
      mal_types.Symbol('atom?'): lambda x: true_false(isinstance(x, mal_types.Atom)),
      mal_types.Symbol('deref'): lambda x: x.get(),
      mal_types.Symbol('reset!'): lambda atom, mal_value: reset(atom, mal_value),
      mal_types.Symbol('swap!'): lambda atom, function, *args: swap(atom, function, *args),

      mal_types.Symbol('cons'): lambda new_element, original_list: mal_types.List([new_element] + original_list.list),
      mal_types.Symbol('concat'): lambda *lists: concat(*lists),
      mal_types.Symbol('vec'): lambda vector: mal_types.Vector(vector.list),
      mal_types.Symbol('nth'): lambda list_type, index: nth(list_type, index),
      mal_types.Symbol('first'): lambda list_type: first(list_type),
      mal_types.Symbol('rest'): lambda list_type: rest(list_type)

      }

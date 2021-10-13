import copy
import operator
import time

from mal_python import mal_types
from mal_python import printer
from mal_python import parser


class IndexOutOfBounds(Exception):
    pass


def true_false(x):
    return mal_types.TrueType() if x else mal_types.FalseType()


def prstr(*items):
    joined_string = " ".join(
        [printer.print_string(item, print_readably=True) for item in items]
    )
    return mal_types.String(joined_string)


def str_function(*items):
    joined_string = "".join(
        [str(printer.print_string(item, print_readably=False)) for item in items]
    )
    return mal_types.String(joined_string)


def prn(*items):
    joined_string = " ".join(
        [str(printer.print_string(item, print_readably=True)) for item in items]
    )
    print(joined_string)
    return mal_types.Nil()


def println(*items):
    joined_string = " ".join(
        [str(printer.print_string(item, print_readably=False)) for item in items]
    )
    print(joined_string)
    return mal_types.Nil()


def slurp(string):
    try:
        with open(str(string), "r") as f:
            return mal_types.String(f.read())
    except FileNotFoundError:
        error_string = f"Could not open file {string}"
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
            if len(mal_type) > 1 and mal_type[0] == "unquote" and not ignore_unquote:
                return mal_type[1]
        except IndexError:
            raise ValueError(f"Cannot quasiquote on List {mal_type}")

        if len(mal_type) == 0:
            return mal_type
        if (
            isinstance(mal_type[0], mal_types.List)
            and len(mal_type[0]) > 1
            and mal_type[0][0] == "splice-unquote"
        ):
            first_element_of_splice = mal_type[0][1]
            return mal_types.List(
                [
                    mal_types.Symbol("concat"),
                    first_element_of_splice,
                    quasiquote(mal_type[1:]),
                ]
            )
        return mal_types.List(
            [
                mal_types.Symbol("cons"),
                quasiquote(mal_type[0]),
                quasiquote(mal_type[1:]),
            ]
        )

    if isinstance(mal_type, mal_types.Vector):
        new_list = mal_types.List(mal_type.list)
        return mal_types.List(
            [mal_types.Symbol("vec"), quasiquote(new_list, ignore_unquote=True)]
        )

    if isinstance(mal_type, mal_types.Symbol) or isinstance(
        mal_type, mal_types.HashMap
    ):
        return mal_types.List([mal_types.Symbol("quote"), mal_type])
    return mal_type


def nth(list_type, index):
    try:
        return list_type[index]
    except IndexError:
        raise IndexOutOfBounds(f"index {index} out of range for List type {list_type}")


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


def make_keyword(value):
    if isinstance(value, mal_types.Keyword):
        return value

    return mal_types.Keyword(":" + value.string)


def throw(err):
    raise mal_types.MalException(err)


def get(hash_map, key):
    try:
        return hash_map.list[hash_map.list.index(key) + 1]
    except AttributeError:  # .list throws (hash_map type doesn't have list member)
        pass
    except ValueError:  # .index throws (key not in hash_map)
        pass

    return mal_types.Nil()


def assoc(hash_map, *args):
    """
    Return a new HashMap, merging new key, value pairs into hash the existing hash_map, taking care to replace new values for exciting keys.
    """
    new_list = list(args)
    for key, value in hash_map.items():
        if key not in new_list[::2]:
            new_list += [key, value]
    return mal_types.HashMap(new_list)


def dissoc(hash_map, *keys):
    new_list = []
    for key, value in hash_map.items():
        if key not in keys:
            new_list += [key, value]

    return mal_types.HashMap(new_list)


def readline(string):
    return mal_types.String(input(string))


def with_meta(mal_type, meta_data):
    copy_of_object = copy.deepcopy(mal_type)
    copy_of_object.meta = meta_data
    return copy_of_object


def meta(mal_type):
    if (
        isinstance(mal_type, mal_types.List)
        or isinstance(mal_type, mal_types.Vector)
        or isinstance(mal_type, mal_types.HashMap)
        or isinstance(mal_type, mal_types.FunctionState)
        or isinstance(mal_type, mal_types.NativeFunction)
    ):
        return mal_type.meta
    return mal_types.Nil()


def ismacro(mal_type):
    if isinstance(mal_type, mal_types.FunctionState) and mal_type.is_macro:
        return True
    return False


def isfn(mal_type):
    if isinstance(mal_type, mal_types.FunctionState):
        return not mal_type.is_macro

    return callable(mal_type)


def conj(mal_type, *args):
    if isinstance(mal_type, mal_types.List):
        return mal_types.List(list(args[::-1]) + mal_type.list)
    elif isinstance(mal_type, mal_types.Vector):
        return mal_types.Vector(mal_type.list + list(args))


def seq(mal_type):
    if len(mal_type) == 0:
        return mal_types.Nil()

    if isinstance(mal_type, mal_types.List):
        return mal_type

    if isinstance(mal_type, mal_types.Vector):  # convert Vector to List
        return mal_types.List(mal_type.list)

    if isinstance(mal_type, mal_types.String):  # convert string to List of characters
        return mal_types.List([mal_types.String(char) for char in mal_type])


namespace = {
    mal_types.Symbol("+"): mal_types.NativeFunction(operator.add),
    mal_types.Symbol("-"): mal_types.NativeFunction(operator.sub),
    mal_types.Symbol("*"): mal_types.NativeFunction(operator.mul),
    mal_types.Symbol("/"): mal_types.NativeFunction(operator.truediv),
    mal_types.Symbol("prn"): lambda *x: prn(*x),
    mal_types.Symbol("list"): lambda *x: mal_types.List(x),
    mal_types.Symbol("list?"): lambda *x: true_false(isinstance(x[0], mal_types.List)),
    mal_types.Symbol("empty?"): lambda *x: true_false(len(x[0]) == 0),
    mal_types.Symbol("count"): lambda *x: len(x[0]),
    mal_types.Symbol("="): lambda *x: true_false(x[0] == x[1]),
    mal_types.Symbol("<"): lambda *x: true_false(x[0] < x[1]),
    mal_types.Symbol("<="): lambda *x: true_false(x[0] <= x[1]),
    mal_types.Symbol(">"): lambda *x: true_false(x[0] > x[1]),
    mal_types.Symbol(">="): lambda *x: true_false(x[0] >= x[1]),
    mal_types.Symbol("pr-str"): lambda *x: prstr(*x),
    mal_types.Symbol("str"): lambda *x: str_function(*x),
    mal_types.Symbol("prn"): lambda *x: prn(*x),
    mal_types.Symbol("println"): lambda *x: println(*x),
    mal_types.Symbol("read-string"): lambda x: parser.parse_string(str(x)),
    mal_types.Symbol("slurp"): lambda x: slurp(x),
    mal_types.Symbol("atom"): lambda x: mal_types.Atom(x),
    mal_types.Symbol("atom?"): lambda x: true_false(isinstance(x, mal_types.Atom)),
    mal_types.Symbol("deref"): lambda x: x.get(),
    mal_types.Symbol("reset!"): lambda atom, mal_value: reset(atom, mal_value),
    mal_types.Symbol("swap!"): lambda atom, function, *args: swap(
        atom, function, *args
    ),
    mal_types.Symbol("cons"): lambda new_element, original_list: mal_types.List(
        [new_element] + original_list.list
    ),
    mal_types.Symbol("concat"): lambda *lists: concat(*lists),
    mal_types.Symbol("vec"): lambda vector: mal_types.Vector(vector.list),
    mal_types.Symbol("nth"): lambda list_type, index: nth(list_type, index),
    mal_types.Symbol("first"): lambda list_type: first(list_type),
    mal_types.Symbol("rest"): lambda list_type: rest(list_type),
    mal_types.Symbol("apply"): lambda function, *args: function(*args[:-1], *args[-1]),
    mal_types.Symbol("map"): lambda function, list_type: mal_types.List(
        [function(item) for item in list_type]
    ),
    mal_types.Symbol("nil?"): lambda mal_type: true_false(
        isinstance(mal_type, mal_types.Nil)
    ),
    mal_types.Symbol("true?"): lambda mal_type: true_false(
        isinstance(mal_type, mal_types.TrueType)
    ),
    mal_types.Symbol("false?"): lambda mal_type: true_false(
        isinstance(mal_type, mal_types.FalseType)
    ),
    mal_types.Symbol("keyword?"): lambda mal_type: true_false(
        isinstance(mal_type, mal_types.Keyword)
    ),
    mal_types.Symbol("symbol?"): lambda mal_type: true_false(
        isinstance(mal_type, mal_types.Symbol)
    ),
    mal_types.Symbol("vector?"): lambda mal_type: true_false(
        isinstance(mal_type, mal_types.Vector)
    ),
    mal_types.Symbol("map?"): lambda mal_type: true_false(
        isinstance(mal_type, mal_types.HashMap)
    ),
    mal_types.Symbol("sequential?"): lambda mal_type: true_false(
        isinstance(mal_type, mal_types.List) or isinstance(mal_type, mal_types.Vector)
    ),
    mal_types.Symbol("symbol"): lambda mal_type: mal_types.Symbol(mal_type.string),
    mal_types.Symbol("vector"): lambda *args: mal_types.Vector(args),
    mal_types.Symbol("keyword"): lambda string: make_keyword(string),
    mal_types.Symbol("hash-map"): lambda *args: mal_types.HashMap(args),
    mal_types.Symbol("assoc"): lambda hash_map, *args: assoc(hash_map, *args),
    mal_types.Symbol("dissoc"): lambda hash_map, *keys: dissoc(hash_map, *keys),
    mal_types.Symbol("throw"): lambda err: throw(err),
    mal_types.Symbol("get"): lambda hash_map, key: get(hash_map, key),
    mal_types.Symbol("contains?"): lambda hash_map, key: true_false(
        key in hash_map.list[::2]
    ),
    mal_types.Symbol("keys"): lambda hash_map: hash_map.keys(),
    mal_types.Symbol("vals"): lambda hash_map: hash_map.values(),
    mal_types.Symbol("readline"): lambda string: readline(string),
    mal_types.Symbol("meta"): lambda mal_type: meta(mal_type),
    mal_types.Symbol("with-meta"): lambda mal_type, meta_data: with_meta(
        mal_type, meta_data
    ),
    mal_types.Symbol("time-ms"): lambda: time.time() * 1000,
    mal_types.Symbol("string?"): lambda mal_type: true_false(
        isinstance(mal_type, mal_types.String)
    ),
    mal_types.Symbol("number?"): lambda mal_type: true_false(
        isinstance(mal_type, mal_types.Int)
    ),
    mal_types.Symbol("fn?"): lambda mal_type: true_false(isfn(mal_type)),
    mal_types.Symbol("macro?"): lambda mal_type: true_false(ismacro(mal_type)),
    mal_types.Symbol("conj"): lambda mal_type, *args: conj(mal_type, *args),
    mal_types.Symbol("seq"): lambda mal_type: seq(mal_type),
}

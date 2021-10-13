closing_paren_style = {"(": ")", "[": "]", "{": "}"}


class MalException(Exception):
    """Exception that stores to be able to use it in a try/catch block"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        if isinstance(self.value, String) or isinstance(self.value, HashMap):
            return f"Exception {repr(self.value)}"

        return repr(self.value)


class UnrecognizedSymbol(Exception):
    pass


class Atom:
    def __init__(self, mal_value):
        self.mal_value = mal_value

    def __repr__(self):
        return f"(atom {self.get()})"

    def get(self):
        return self.mal_value

    def set(self, mal_value):
        self.mal_value = mal_value


class Nil:
    def __repr__(self):
        return "nil"

    def __len__(self):
        return 0

    def __eq__(self, other):
        return isinstance(other, Nil)


class TrueType:
    def __repr__(self):
        return "true"

    def __eq__(self, other):
        return isinstance(other, TrueType)

    def __bool__(self):
        return True


class FalseType:
    def __repr__(self):
        return "false"

    def __eq__(self, other):
        return isinstance(other, FalseType)

    def __bool__(self):
        return False


class Int(int):
    def __new__(cls, value):
        return int.__new__(cls, value)


class String:
    def __init__(self, *args):
        self.string = str(*args)

    def __eq__(self, other):
        if isinstance(other, String):
            return self.string == other.string
        elif isinstance(other, str):
            return self.string == other
        return False

    def __iter__(self):
        for item in self.string:
            yield item

    def __len__(self):
        return len(self.string)

    def __repr__(self):
        return self.string


class Symbol:
    def __init__(self, string=""):
        self.string = string

    def __eq__(self, other):
        if isinstance(other, Symbol) or isinstance(other, str):
            return self.string == other
        return False

    def __hash__(self):
        return hash(self.string)

    def __repr__(self):
        return self.string


class ListVariant:
    def __init__(self, *args):
        self.list = list(*args)
        self.meta = Nil()

    def append(self, item):
        self.list.append(item)

    def __eq__(self, other):
        return self.list == other

    def __iter__(self):
        for item in self.list:
            yield item

    def __len__(self):
        return len(self.list)

    def __repr__(self):
        return " ".join([repr(x) for x in self.list])


class Keyword:
    def __init__(self, string):
        self.string = string

    def __eq__(self, other):
        return isinstance(other, Keyword) and self.string == other.string

    def __hash__(self):
        return hash(self.string)

    def __repr__(self):
        return self.string


class List(ListVariant):
    open_paren = "("
    close_paren = ")"

    def __init__(self, *args):
        super().__init__(*args)

    def __getitem__(self, indices):
        if isinstance(indices, slice):
            return List([item for item in self.list[indices]])
        return self.list[indices]

    def __hash__(self):
        return hash(tuple(self.list))

    def __repr__(self):
        return self.open_paren + super().__repr__() + self.close_paren

    def index(self, index):
        return self.list.index(index)


class Vector(ListVariant):
    open_paren = "["
    close_paren = "]"

    def __init__(self, *args):
        super().__init__(*args)

    def __getitem__(self, indices):
        if isinstance(indices, slice):
            return Vector([item for item in self.list[indices]])
        return self.list[indices]

    def __hash__(self):
        return hash(tuple(self.list))

    def __repr__(self):
        return self.open_paren + super().__repr__() + self.close_paren

    def index(self, index):
        return self.list.index(index)


class HashMap(ListVariant):
    open_paren = "{"
    close_paren = "}"

    def __init__(self, *args):
        super().__init__(*args)

    def __getitem__(self, indices):
        if isinstance(indices, slice):
            return HashMap([item for item in self.list[indices]])
        return self.list[indices]

    def __eq__(self, other):
        return (
            isinstance(other, HashMap)
            and set(self.keys()) == set(other.keys())
            and set(self.values()) == set(other.values())
        )

    def __hash__(self):
        return hash(tuple(self.list))

    def __repr__(self):
        return self.open_paren + super().__repr__() + self.close_paren

    def items(self):
        return List(zip(self.keys(), self.values()))

    def keys(self):
        return List(self.list[::2])

    def values(self):
        return List(self.list[1::2])


class FunctionState:
    def __init__(self, mal_type, params, env, fn, is_macro=FalseType()):
        self.mal_type = mal_type
        self.params = params
        self.env = env
        self.fn = fn
        self.is_macro = is_macro
        self.meta = Nil()

    def __call__(self, *args):
        return self.fn(*args)


class NativeFunction:
    def __init__(self, function):
        self.function = function
        self.meta = Nil()

    def __call__(self, *args):
        return Int(self.function(*args))

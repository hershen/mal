closing_paren_style = {'(': ')',
                       '[': ']',
                       '{': '}'}

class Atom:
    def __init__(self, mal_value):
        self.mal_value = mal_value

    def __repr__(self):
        return f'(atom {self.get()})'

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

class true:
    def __repr__(self):
        return 'true'
    
    def __eq__(self, other):
        return isinstance(other, true)

    def __bool__(self):
        return True

class false:
    def __repr__(self):
        return 'false'

    def __eq__(self, other):
        return isinstance(other, false)

    def __bool__(self):
        return False

class Int(int):
    def __new__(cls, value):
        return int.__new__(cls, value)

class String():
    def __eq__(self, other):
        if isinstance(other, String):
            return self.string == other.string
        elif isinstance(other, str):
            return self.string == other
        return False

    def __init__(self, *args):
        self.string = str(*args)

    def __iter__(self):
        for item in self.string:
            yield item

    def __repr__(self):
        return '"' + str(self.string) + '"'

    def __str__(self):
        return self.string

class Symbol():
    def __init__(self, string=''):
        self.string = string

    def __repr__(self):
        return self.string

    def __eq__(self, other):
        if isinstance(other, Symbol):
            return self.string == other
        elif isinstance(other, str):
            return self.string == other
        return False

    def __hash__(self):
        return hash(self.string)

class List_variant():
    def __init__(self, *args):
        self.list = list(*args)
    
    def __iter__(self):
        for item in self.list:
            yield item

    def __len__(self):
        return len(self.list)

    def __repr__(self):
        return ' '.join([repr(x) for x in self.list])

    def append(self, item):
        self.list.append(item)

    def __eq__(self, other):
        return self.list == other

class List(List_variant):
    open_paren = '('
    close_paren = ')'
    def __getitem__(self, indices):
        if isinstance(indices, slice):
            return List([item for item in self.list[indices]])
        return self.list[indices]

    def __init__(self, *args):
        super().__init__(*args)

    def __repr__(self):
        return self.open_paren + super().__repr__() + self.close_paren

    def index(self, index):
        return self.list.index(index)

class Vector(List_variant):
    open_paren = '['
    close_paren = ']'
    def __getitem__(self, indices):
        if isinstance(indices, slice):
            return Vector([item for item in self.list[indices]])
        return self.list[indices]

    def __init__(self, *args):
        super().__init__(*args)

    def __repr__(self):
        return self.open_paren + super().__repr__() + self.close_paren

class Hash_map(List_variant):
    open_paren = '{'
    close_paren = '}'
    def __getitem__(self, indices):
        if isinstance(indices, slice):
            return Hash_map([item for item in self.list[indices]])
        return self.list[indices]

    def __init__(self, *args):
        super().__init__(*args)

    def __repr__(self):
        return self.open_paren + super().__repr__() + self.close_paren

class FunctionState:
    def __init__(self, mal_type, params, env, fn, is_macro=false):
        self.mal_type = mal_type
        self.params = params
        self.env = env
        self.fn = fn
        self.is_macro = is_macro

    def __call__(self, *args):
        return self.fn(*args)



closing_paren_style = {'(': ')',
                       '[': ']',
                       '{': '}'}

class Int(int):
    def __new__(cls, value):
        return int.__new__(cls, value)

class String(str):
    def __init(self, *args):
        str.__init(self, *args)


class List_variant(list):
    def __init__(self, *args):
        list.__init__(self, *args)
    
    def __str__(self):
        the_list = [*self]
        return the_list[0] + ' '.join([str(x) for x in the_list[1:-1]]) + the_list[-1]

class List(List_variant):
    def __init__(self, *args):
        super().__init__(*args)

class Vector(List_variant):
    def __init__(self, *args):
        super().__init__(*args)

class Hash_map(List_variant):
    def __init__(self, *args):
        super().__init__(*args)

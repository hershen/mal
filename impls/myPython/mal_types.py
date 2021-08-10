closing_paren_style = {'(': ')',
                       '[': ']',
                       '{': '}'}

class Int(int):
    def __new__(cls, value):
        return int.__new__(cls, value)

class String(str):
    def __init__(self, *args):
        str.__init__(*args)

class List_variant(list):
    def __init__(self, *args):
        list.__init__(self, *args)
    
    def __str__(self):
        the_list = [*self]
        return ' '.join([str(x) for x in the_list])

class List(List_variant):
    open_paren = '('
    close_paren = ')'
    def __init__(self, *args):
        super().__init__(*args)

    def __str__(self):
        return self.open_paren + super().__str__() + self.close_paren

class Vector(List_variant):
    open_paren = '['
    close_paren = ']'
    def __init__(self, *args):
        super().__init__(*args)

    def __str__(self):
        return self.open_paren + super().__str__() + self.close_paren

class Hash_map(List_variant):
    open_paren = '{'
    close_paren = '}'
    def __init__(self, *args):
        super().__init__(*args)

    def __str__(self):
        return self.open_paren + super().__str__() + self.close_paren

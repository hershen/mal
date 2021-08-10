closing_paren_style = {'(': ')',
                       '[': ']',
                       '{': '}'}

class Int(int):
    def __new__(cls, value):
        return int.__new__(cls, value)

class String():
    def __init__(self, *args):
        self.string = str(*args)

    def __str__(self):
        return self.string

    def __eq__(self, other):
        return self.string == other

class Symbol():
    def __init__(self, string=''):
        self.string = string

    def __str__(self):
        return self.string

    def __eq__(self, other):
        return self.string == other

    def __hash__(self):
        return hash(self.string)

class List_variant():
    def __getitem__(self, indices):
        return self.list[indices]

    def __init__(self, *args):
        self.list = list(*args)
    
    def __iter__(self):
        for item in self.list:
            yield item

    def __len__(self):
        return len(self.list)

    def __str__(self):
        return ' '.join([str(x) for x in self.list])

    def append(self, item):
        self.list.append(item)

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

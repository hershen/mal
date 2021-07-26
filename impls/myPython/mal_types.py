closing_paren_style = {'(': ')',
                       '[': ']'}

class Int(int):
    def __new__(cls, value):
        return int.__new__(cls, value)

class String(str):
    def __init(self, *args):
        str.__init(self, *args)

class List(list):
    def __init__(self, *args):
        list.__init__(self, *args)
    
    def __str__(self):
        return '(' + ' '.join([str(x) for x in [*self][1:-1]]) + ')'

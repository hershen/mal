
class List(list):
    def __init__(self, *args):
        list.__init__(self, *args)
    
    def __str__(self):
        return '(' + ' '.join([str(x) for x in [*self][1:-1]]) + ')'

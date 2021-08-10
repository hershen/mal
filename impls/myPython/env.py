
class MissingKeyInEnvironment(Exception):
    pass

class Env:
    def __init__(self, outer):
        self.outer = outer
        self.data = {}

    def set(self, key, value):
        self.data[key] = value

    def find(self, key):
        if key in self.data:
            return self

        if self.outer == 'nil':
            raise MissingKeyInEnvironment(f'{key} not found')

        return self.outer.find(key)
    
    def get(self, key):
        try:
            return self.find(key).data[key]
        except KeyError:
            raise MissingKeyInEnvironment(f'{key} not found')


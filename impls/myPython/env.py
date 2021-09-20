import mal_types


class MissingKeyInEnvironment(Exception):
    pass


class Env:
    def __init__(self, outer, binds=[], exprs=[]):
        self.outer = outer
        if "&" in binds:
            ampersand_index = binds.index("&")
            self.data = {
                key: expr
                for key, expr in zip(binds[:ampersand_index], exprs[:ampersand_index])
            }
            self.data[binds[ampersand_index + 1]] = exprs[ampersand_index:]
        else:
            self.data = {key: expr for key, expr in zip(binds, exprs)}

    def set(self, key, value):
        self.data[key] = value

    def find(self, key):
        if key in self.data:
            return self

        if isinstance(self.outer, mal_types.Nil):
            raise MissingKeyInEnvironment(f"'{key}' not found")

        return self.outer.find(key)

    def get(self, key):
        try:
            return self.find(key).data[key]
        except KeyError:
            raise MissingKeyInEnvironment(f"'{key}' not found")

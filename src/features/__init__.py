class Feature(dict):
    def __init__(self, name, ident, **kwargs):
        self.name = name
        self.ident = ident
        self.update(kwargs)

    def distance_to(self, other, maxima=None):
        res = 1.
        for key in self.keys():
            mine, others, maximum = self[key], other[key]
            if isinstance(mine, str):
                pass
            if type(mine) is not type(others):
                raise TypeError
            if maxima is None:
                res *= float(others - mine) / max(others, mine)
            else:
                maximum = maxima[key]
                res *= float(others - mine) / maximum
        return res

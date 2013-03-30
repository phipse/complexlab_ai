class Feature(dict):
    def __init__(self, name, **kwargs):
        self.name = name
        self.update(kwargs)

    def distance_to(self, other, maxima=None):
        res = 1.
        for key in self.keys():
            mine, others, maximum = self[key], other[key], maxima[key]
            if isinstance(mine, str):
                pass
            if type(mine) is not type(others):
                raise TypeError
            if maxima is None:
                res *= float(others - mine) / max(others, mine)
            else:
                res *= float(others - mine) / maximum
        return res

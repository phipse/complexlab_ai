class Feature:
    name = None # name of the feature, e.g. "Monotony"

    @classmethod
    def initialize(cls, default_id_ranges, opts = {}):
        if not isinstance(default_id_ranges, list): raise TypeError, "default_id_ranges must be a list"
        cls.default_id_ranges = default_id_ranges

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        if not isinstance(id, list) or len(default_id_ranges) != len(id):
            raise ValueError, "id must be a list and have the same length like default_id_ranges"
        self._id = id

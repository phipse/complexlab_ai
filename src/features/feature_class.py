class FeatureClass:
    def __init__(self, name, default_attr_ranges, opts = {}):
        if not isinstance(default_attr_ranges, list): raise TypeError, "default_attr_ranges must be a list"
        self.default_attr_ranges = default_attr_ranges
        self.name = name

    def create_feature(attributes):
        if not isinstance(attributes, list) or len(self.default_attr_ranges) != len(id):
            raise ValueError, "id must be a list and have the same length like default_id_ranges"
        return Feature(attributes, self)

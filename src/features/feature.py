class Feature:
    def __init__(self, attributes, feature_group):
        self.attributes = attributes
        self.feature_group = feature_group

    @property
    def name(self):
        self.feature_group.name

    @property
    def default_attr_ranges(self):
        self.feature_class.default_attr_ranges

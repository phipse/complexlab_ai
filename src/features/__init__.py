import feature_class

class Feature:
    def __init__(attributes, feature_class):
        self.attributes = attributes
        self.feature_class = feature_class

    @property
    def name(self):
        self.feature_class.name

    @property
    def default_attr_ranges(self):
        self.feature_class.default_attr_ranges

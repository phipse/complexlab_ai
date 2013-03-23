from feature import Feature

class FeatureGroup:
    def __init__(self, name, default_attr_ranges, opts = {}):
        if not isinstance(default_attr_ranges, list): 
	  raise TypeError, "default_attr_ranges must be a list"
        self.default_attr_ranges = default_attr_ranges
        self.name = name

    def create_feature(self, attributes):
      if not isinstance(attributes, list) or (isinstance(attributes, list) and len(self.default_attr_ranges) != len(attributes)):
          raise ValueError, "in FeatureGroup: attributes must be a list and have the same length like default_attr_ranges"
      return Feature(attributes, self)

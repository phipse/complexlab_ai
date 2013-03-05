from feature import Feature

class FeatureClass:
    def __init__(self, name, default_attr_ranges, opts = {}):
        if not isinstance(default_attr_ranges, list): 
	  raise TypeError, "default_attr_ranges must be a list"
        self.default_attr_ranges = default_attr_ranges
        self.name = name

    def create_feature(self, attributes):
        
      # what shall the OR part check? I get a TypeError: object of type
      # 'builtin_function_or_method' has no len() --phi
      if not isinstance(attributes, list): #or len(self.default_attr_ranges) != len(id):
            raise ValueError, "id must be a list and have the same length like default_id_ranges"
      return Feature(attributes, self)

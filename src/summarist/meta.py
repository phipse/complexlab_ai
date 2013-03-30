class Meta(object):
    def __init__(self, feature_group, db):
        self.db = db
        self.feature_group = feature_group
        self.data = db.meta.find_one({"name": feature_group.name})
        if(self.data == None):
            self.data = {"name": feature_group.name, "attr_ranges" : feature_group.default_attr_ranges} # using _id because it is indexed by default
	    # replaced with name, because a consistent naming scheme is
	    # necessary for the grouper --phi

    def attr_ranges(self):
        return self.data['attr_ranges']

    def feature_group_name(self):
        return self.data['name']

    def learn_from_attributes(self, attributes):
        for i in range(0, len(attributes)-1):
            if self.feature_group.default_attr_ranges[i] == None: # only update attribute_range if not initially specified by user (via feature-config)
                if self.data['attr_ranges'][i] == None:
                    self.data['attr_ranges'][i] = [attributes[i], attributes[i]] # [min, max]
                elif attributes[i] < self.data['attr_ranges'][i][0]: # update min?
                    self.data['attr_ranges'][i][0] = attributes[i]
                elif attributes[i] > self.data['attr_ranges'][i][1]: # update max?
                    self.data['attr_ranges'][i][1] = attributes[i]

    def save(self):
        self.db.meta.save(self.data)

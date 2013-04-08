import logging

class Meta(object):
    @classmethod
    def create(cls, name, default_attr_ranges, merge_threshold, db):
        data = { "name": name, "default_attr_ranges": default_attr_ranges, "attr_ranges": default_attr_ranges, "merge_threshold": merge_threshold }
        db.meta.insert(data)

    def __init__(self, name, db):
        self.db = db
        self.data = db.meta.find_one({"name": name})
        if not self.data:
            logging.error("Access to non-existant Meta-Object with name: %s" % name)
            exit(1)

    def attr_ranges(self):
        return self.data['attr_ranges']

    def feature_group_name(self):
        return self.data['name']

    def learn_from_attributes(self, attributes):
        for i in range(0, len(attributes)-1):
            if self.data["default_attr_ranges"][i] == None: # only update attribute_range if not initially specified by user (via feature-config)
                if self.data['attr_ranges'][i] == None:
                    self.data['attr_ranges'][i] = [attributes[i], attributes[i]] # [min, max]
                elif attributes[i] < self.data['attr_ranges'][i][0]: # update min?
                    self.data['attr_ranges'][i][0] = attributes[i]
                elif attributes[i] > self.data['attr_ranges'][i][1]: # update max?
                    self.data['attr_ranges'][i][1] = attributes[i]

    def save(self):
        self.db.meta.save(self.data)

import logging
import sys

class Meta(object):
    @classmethod
    def create(cls, name, default_attr_ranges, merge_frequency, merge_threshold, db):
        data = { "name": name, "default_attr_ranges": default_attr_ranges, "attr_ranges": default_attr_ranges, "merge_frequency": merge_frequency, "merge_threshold": merge_threshold }
        db.meta.insert(data)

    def __init__(self, name, db):
        self.db = db
        self.data = db.meta.find_one({"name": name})
        if not self.data:
            logging.fatal("Access to non-existant Meta-Object with name: %s" % name)
            sys.exit(1)

    def get_merge_frequency(self):
        return self.data['merge_frequency']

    def get_merge_threshold(self):
        return self.data['merge_threshold']

    def get_attr_ranges(self):
        return self.data['attr_ranges']

    def attr_ranges(self):
        return self.data['attr_ranges']

    def feature_group_name(self):
        return self.data['name']

    def learn_from_attributes(self, attributes):
        for attr in attributes:
            dar= self.data["default_attr_ranges"]
            if not dar.has_key(attr) or dar[attr] == None: # only update attribute_range if not initially specified by user (via feature-config)
                if self.data['attr_ranges'][attr] == None:
                    self.data['attr_ranges'][attr] = [attributes[attr], attributes[attr]] # [min, max]
                elif attributes[attr] < self.data['attr_ranges'][attr][0]: # update min?
                    self.data['attr_ranges'][attr][0] = attributes[attr]
                elif attributes[attr] > self.data['attr_ranges'][attr][1]: # update max?
                    self.data['attr_ranges'][attr][1] = attributes[attr]

    def save(self):
        self.db.meta.save(self.data)

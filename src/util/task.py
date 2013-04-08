import json
import logging

class Task(object):
    def check_api(self, api):
        if not 'name' in api:
            raise SyntaxError("Error parsing task: api without a 'name'")
        if not 'features_to_observe' in api:
            raise SyntaxError("Error parsing task: no 'features_to_observe' in API '%s' specfied" % api['name'])

    def check_fto(self, api, fto):
        if not 'type' in fto:
            raise SyntaxError("feature_to_observe without a type in API '%s'" % api['name'])
        if not 'default_attr_ranges' in fto:
            raise SyntaxError("Error parsing task: no 'default_attr_ranges' in feature '%s' specified" % fto['type'])
        if not 'merge_threshold' in fto:
            raise SyntaxError("Error parsing task: no 'merge_threshold' in feature '%s' specified" % fto['type'])
        if not 'options' in fto:
            raise SyntaxError("Error parsing task: no 'options' in feature '%s' specified" % fto['type'])

    def __init__(self, path):
        self.mask_names = []
        self.default_attr_ranges = {}
        self.merge_thresholds = {}
        logging.debug("Loading json %s", path)
        task = json.load(open(path, "r"))
        if 'name' not in task:
            raise SyntaxError("Error parsing task: no 'name' specified")
        self.name = task['name'].strip()
        if 'apis' not in task:
            raise SyntaxError("Error parsing task: no 'apis' specfied")
        for api in task['apis']:
            self.check_api(api)
            for fto in api['features_to_observe']:
                self.check_fto(api, fto)
                self.mask_names.append(fto["type"].strip())
                self.default_attr_ranges[fto["type"].strip()] = fto["default_attr_ranges"]
                self.merge_thresholds[fto["type"].strip()] = fto["merge_threshold"]

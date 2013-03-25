import json
import sys
from features import FeatureGroup
from extractor.masks import *

class Task(object):
    def check_api(self, api):
        if not 'name' in api: sys.exit("Error parsing config: api without a 'name'")
        if not 'features_to_observe' in api: sys.exit("Error parsing config: no 'features_to_observe' in API '%s' specfied" % api['name'])

    def check_fto(self, api, fto):
        if not 'type' in fto:
            sys.exit("feature_to_observe without a type in API '%s'" % api['name'])
        if not 'default_attr_ranges' in fto:
            sys.exit("Error parsing config: no 'default_attr_ranges' in feature '%s' specified" % fto['type'])
        if not 'options' in fto:
            sys.exit("Error parsing config: no 'options' in feature '%s' specified" % fto['type'])

    def __init__(self, path):
        self.tasks = []
        task = json.load(open(path))
        if not 'apis' in task: sys.exit("Error parsing config: no 'apis' specfied")
        for api in task['apis']:
            self.check_api(api)
            for fto in api['features_to_observe']:
                self.check_fto(api, fto)
                mask_gen = getattr(globals()[fto['type'].split('.')[0]], fto['type'].split('.')[1])
                feature_group = FeatureGroup(fto['type'], fto['default_attr_ranges'], fto['options'])
                self.tasks.append({"feature_group": feature_group, "mask_gen": mask_gen})

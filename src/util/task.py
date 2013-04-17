import json
import logging
import extractor
import sys
from operator import itemgetter

class Task(object):
    def check_api(self, api):
        if not 'name' in api:
            raise SyntaxError("Error parsing task: api without a 'name'")
        if not 'features_to_observe' in api:
            raise SyntaxError("Error parsing task: no 'features_to_observe' in API '%s' specfied" % api['name'])

    def check_fto(self, api, fto):
        if not 'mask_group' in fto:
            raise SyntaxError("feature_to_observe without a 'mask_group' in API '%s'" % api['name'])
        if not 'default_attr_ranges' in fto:
            raise SyntaxError("Error parsing task: no 'default_attr_ranges' in feature '%s' specified" % fto['type'])
        if not 'merge_frequency' in fto:
            raise SyntaxError("Error parsing task: no 'merge_frequency' in feature '%s' specified" % fto['type'])
        if not 'merge_threshold' in fto:
            raise SyntaxError("Error parsing task: no 'merge_threshold' in feature '%s' specified" % fto['type'])
        if not 'options' in fto:
            raise SyntaxError("Error parsing task: no 'options' in feature '%s' specified" % fto['type'])

    def __init__(self, path):
        self.masks = []
        self.mask_groups = []

        logging.debug("Loading json %s", path)
        try:
            task = json.load(open(path, "r"))
        except ValueError:
            logging.fatal("Error parsing task: Invalid Syntax of JSON file")
            sys.exit(1)

        if 'name' not in task:
            raise SyntaxError("Error parsing task: no 'name' specified")
        self.name = task['name'].strip()
        if 'apis' not in task:
            raise SyntaxError("Error parsing task: no 'apis' specfied")
        for api in task['apis']:
            self.check_api(api)
            for fto in api['features_to_observe']:
                self.check_fto(api, fto)
                fto["mask_group"] = fto["mask_group"].strip()
                self.mask_groups.append(fto["mask_group"])
                for mask_name in [x().name for x in extractor.masks.get_all_masks([fto["mask_group"]])]:
                    self.masks.append(dict(fto.items() + {"mask_name": mask_name}.items()))

    def get_masks_by_mask_group(self, type):
        return filter(lambda x: x['mask_group'] == type, self.masks)

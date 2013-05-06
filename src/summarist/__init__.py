from sys import exit
import logging
from pymongo import Connection
import bson
import datetime
from features import Feature

from summarist.meta import Meta

class Summarist(object):
    def __init__(self, masks, connection=None):
        if connection is None:
            try:
                connection = Connection()
            except Exception, e:
                logging.fatal(e)
                exit(1)
        self.db = connection.ai

        # TODO ask if data should be removed
        self.db.meta.remove()
        self.db.features.remove()
        self.db.characteristics.remove()

        for mask in masks:
            Meta.create(mask['mask_name'], mask['default_attr_ranges'], mask['merge_frequency'], mask['merge_threshold'], self.db)

    def insert_feature(self, feature):
        logging.debug("inserting %s", feature)
        dummyTime = datetime.time()
        for attr in feature:
            if type(feature[attr]) == datetime.date:
                feature[attr] = datetime.datetime.combine(feature[attr], dummyTime)
            #else:
                #feature[attr] = bson.BSON(feature[attr])
        entry = {"name": feature.name, "ident": feature.ident, "attributes": feature} # TODO ensureIndex on name
        logging.debug(entry)
        self.db.features.insert(feature.db_entry())

    def update_characteristics(self, name, merge_frequency):
        features = self.db.features.find({"name": name})

        start = features.count() - merge_frequency
        logging.debug("Updating characteristics with features %i to %i of type %s" % (start+1, start+merge_frequency, name,))

        for feature in features.skip(start):
            self.db.characteristics.insert(feature)

    def merge_characteristics(self, name, merge_threshold): # returns if one or more characteristics were merged (boolean)
        logging.debug("Merging characterics")
        characteristics = self.db.characteristics.find({"name": name})
        meta = Meta(name, self.db)

        chars = list(characteristics)

        # find "best fit" (other characteristic with minimal distance) for each characteristic
        best_fits = [None]*len(chars) #  list of tuples: (index of best fit, distance)
        best_distance = 1.
        for first_i, first in enumerate(chars):
            for second_i, second in enumerate(chars):
                if first['_id'] is not second['_id']:
                    distance = Feature.from_db(first).distance_to(Feature.from_db(second), meta.get_attr_ranges())
                    if (not best_fits[first_i]) or (distance < best_fits[first_i][2]):
                        best_fits[first_i] = (first_i, second_i, distance)
                        if distance < best_distance: best_distance = distance

        if best_distance > (1-merge_threshold): return False # signalize that no characteristic needed to be merged
        
        for bf in best_fits:
            if not bf: continue # continue if first has been merged before
            if not best_fits[bf[1]]: continue # continue if second has been merged before

            first = Feature.from_db(chars[bf[0]])
            second = Feature.from_db(chars[bf[1]])

            first.merge(second)
            self.db.characteristics.save(first.db_entry())
            self.db.characteristics.remove({"_id": second._id})
            best_fits[bf[0]] = None

            # TODO recalculate best_fits with same bf[0]

        return True # signalize that one or more characteristics were merged

    def process(self, new_features):
        for feature in new_features:
            self.insert_feature(feature)

            # update meta-object
            meta = Meta(feature.name, self.db)
            meta.learn_from_attributes(feature)
            meta.save()

            features = self.db.features.find({"name": feature.name})
            if(features.count() % meta.get_merge_frequency() == 0):
                logging.debug("Summarizing %s" % feature.name)

                # insert new features as "characteristics"
                self.update_characteristics(feature.name, meta.get_merge_frequency())

                # merge characteristics
                while True:
                    changed = self.merge_characteristics(feature.name, meta.get_merge_threshold())
                    if not changed: break
        return True

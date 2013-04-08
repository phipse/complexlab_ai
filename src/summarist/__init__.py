from sys import exit
import logging
from pymongo import Connection
import bson
import datetime

from summarist.meta import Meta

class Summarist(object):
    def __init__(self, all_default_attr_ranges, connection=None):
        if connection is None:
            try:
                connection = Connection()
            except Exception, e:
                logging.fatal(e)
                exit(1)
        self.db = connection.ai

        for name, default_attr_ranges in all_default_attr_ranges.iteritems():
            Meta.create(name, default_attr_ranges, self.db)

    def insert_feature(self, feature):
        logging.debug("inserting %s", feature)
        dummyTime = datetime.time()
        for attr in feature:
            if type(feature[attr]) == datetime.date:
                feature[attr] = datetime.datetime.combine(feature[attr], dummyTime)
            #else:
                #feature[attr] = bson.BSON(feature[attr])
        entry = {"name": feature.name, "attributes": feature} # TODO ensureIndex on name
        logging.debug(entry)
        self.db.features.insert(entry)

    def process(self, features):
        for feature in features:
            self.insert_feature(feature)
            if(self.db.features.find({"name": feature.name}).count() % 1000 == 0):
                logging.debug("Summarizing %s" % feature.name)

                # update meta-object
                meta = Meta(feature.name, self.db) # get or create meta object of feature group
                meta.learn_from_attributes(feature.attributes)
                meta.save()

                # aggregate to characteristics, if possible async
                # merge characteristics, if possible async. lock!
        return True

    def serializeDateTime(self, date):
      str(date)

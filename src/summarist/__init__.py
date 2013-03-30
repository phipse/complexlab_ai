from sys import exit
import logging
from pymongo import Connection

from summarist.meta import Meta

class Summarist(object):
    def __init__(self, connection=None):
        if connection is None:
            try:
                connection = Connection()
            except Exception, e:
                logging.fatal(e)
                exit(1)
        self.db = connection.ai

    def process(self, features):
        for feature in features:
            logging.debug("inserting %s", feature)
            self.db.features.insert({"name": feature.name, "attributes": str(feature)}) # TODO ensureIndex on name, remove str if possible
            if(self.db.features.find({"name": feature.name}).count() % 1000 == 0):
                # update meta-object
                meta = Meta(feature.name, self.db) # get or create meta object of feature group
                meta.learn_from_attributes(feature.attributes)
                meta.save()

                # aggregate to characteristics, if possible async
                # merge characteristics, if possible async. lock!
        return True

    def serializeDateTime(self, date):
      str(date)

from pymongo import Connection

class Summarist:
    def __init__(self, connection = Connection()):
        self.db = connection.ai

    def process(self, features):
        for feature in features:
            self.db.features.insert({"name": feature.name, "attributes": str(feature.attributes)}) # TODO ensureIndex on name, remove str if possible
            if(self.db.features.count() % 1000 == 0):
                # update meta-object
                meta = Meta(feature.feature_group.name, self.db) # get or create meta object of feature group
                meta.learn_from_attributes(feature.attributes)
                meta.save()

                # aggregate to characteristics, if possible async
                # merge characteristics, if possible async. lock!
        return True

    def serializeDateTime(self, date):
      str(date)

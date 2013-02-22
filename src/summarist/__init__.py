from pymongo import Connection

class Summarist:
    def __init__(self):
        connection = Connection()
        self.db = connection.ai

    def process(self, features):
        for feature in features:
            db.features.insert({"name": feature.name, "attributes": feature.attributes}) # TODO ensureIndex(name, id)
            if db.features.count % 1000:
                # update meta-object
                meta = db.meta.find_one({"_id": feature.name})
                default_attr_ranges = feature.default_attr_ranges
                if(meta == None):
                    meta = {"_id": feature.name, "attr_ranges" : default_attr_ranges} # using _id because it is indexed by default
                for i in range(0, len(feature.attributes)-1):
                    if meta.attr_ranges[i] == None: # create meta object for feature-name
                        meta.attr_ranges[i] == [feature.attributes[i], feature.attributes[i]] # [min, max]
                    elif(default_attr_ranges[i] == None): # only update meta object if not specified by user (via feature-config)
                        if feature.attributes[i] < meta.attr_ranges[i]: # update min?
                            meta.attr_ranges[i][0] = feature.attributes[i]
                        elif feature.attributes[i] > meta.attr_ranges[i]: # update max?
                            meta.attr_ranges[i][1] = feature.attributes[i]
                db.meta.save(meta)

                # aggregate to characteristics, if possible async
                # merge characteristics, if possible async. lock!

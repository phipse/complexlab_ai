from pymongo import Connection

class Summarist:
    def __init__(self):
        connection = Connection()
        self.db = connection.ai

    def process(self, id, features):
        for feature in features:
            db.features.insert({"name": feature.name, "id": feature.id}) # TODO ensureIndex(name, id)
            if db.features.count % 1000:
                # update meta-object
                meta = db.meta.find_one({"_id": feature.name})
                default_id_ranges = feature.__class__.default_id_ranges
                if(meta == None):
                    meta = {"_id": feature.name, "id_ranges" : default_id_ranges} # using _id because it is indexed by default
                for i in range(0, len(feature.id)-1):
                    if meta.id_ranges[i] == None: # create meta object for feature-name
                        meta.id_ranges[i] == [feature.id[i], feature.id[i]] # [min, max]
                    elif(default_id_ranges[i] == None): # only update meta object if not specified by user (via feature-config)
                        if feature.id[i] < meta.id_ranges[i]: # update min?
                            meta.id_ranges[i][0] = feature.id[i]
                        elif feature.id[i] > meta.id_ranges[i]: # update max?
                            meta.id_ranges[i][1] = feature.id[i]
                db.meta.save(meta)

                # aggregate to characteristics, if possible async
                # merge characteristics, if possible async. lock!

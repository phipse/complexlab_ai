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
                    if(default_id_ranges[i] == None):
                        # update meta.ranges[i]
                        if meta.id_ranges[i] == None:
                            meta.id_ranges[i] == {"min": feature.id[i], "max": feature.id[i]}
                        else:
                            if feature.id[i] < meta.id_ranges[i]:
                                meta.id_ranges[i].min = feature.id[i]
                            elif feature.id[i] > meta.id_ranges[i]:
                                meta.id_ranges[i].max = feature.id[i]
                db.meta.save(meta)

                # aggregate to characteristics, if possible async
                # merge characteristics, if possible async. lock!

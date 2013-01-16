from pymongo import MongoClient

class Summarizer:
    def __init__(self):
        connection = MongoClient()
        self.db = connection.complexlab_ai

    def process(self, id, features):
        for feature in features:
            cs = Characteristic.load(self.db, feature.name)
            fits = [c for c in cs if c.similarity_to(feature) > 0.9]
            for fit in fits: c.insert(feature)
            db.characteristics.save(fits)

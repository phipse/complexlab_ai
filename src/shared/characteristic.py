class Characteristic:
    d = {} # may/should include name, ( min,max,mean | value ), count, datasets (array)
    
    @classmethod
    def load(db):
        cs = db.characteristics.find({"name": feature.name})
        result = [Characteristic(c) for c in cs]

    def __init__(self, data):
        defaults = {count: 0, datasets: []}
        self.d = dict(defaults + data)

    # decides whether a feature fits to the characteristic in a rating from 0 to 1
    def similarity_to(self, feature):
        if feature.type == 'enumerable':
            if feature.value_in_range(self.d.min, self.d.max): return 1.0
            elif feature.value < self.d.min: diff = self.d.min - feature.value
            else: diff = feature.value - self.d.max
            return diff #TODO
        else:
            if self.d.value == feature.value: return 1.0
        return 0

    # expands characteristic by given feature
    def insert(self, id, feature):
        self.d.count += 1
        self.d.dataset.append(id)

        if feature.type == 'enumerable':
            if (self.d.min and self.d.min > feature.value) or not self.d.min: self.d.min = feature.value
            if (self.d.max and self.d.min < feature.value) or not self.d.max: self.d.max = feature.value

            if not self.d.mean: self.d.mean = feature.value
            else: self.d.mean = self.d.count / (self.d.count+1) * self.d.mean + feature.value / (self.d.count+1)
    def save(self, db):
        db.characteristics.save(self.d)

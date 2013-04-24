import datetime
import time

class Feature(dict):
    def __init__(self, name, ident, **kwargs):
        self._id = None # database id
        self.name = name
        if not isinstance(ident, list):
            ident = [ident]
        self.ident = ident
        self.attributes = kwargs

    def __getitem__(self, key):
        return self.attributes[key]

    def __setitem__(self, key, value):
        self.attributes[key] = value

    def __delitem__(self, key):
        del self.attributes[key]

    def __iter__(self):
        return iter(self.attributes)

    def __len__(self):
        return len(self.attributes)

    @classmethod
    def from_db(cls, d):
        name = d['name']
        ident = d['ident']
        feature = Feature(name, ident, **d['attributes'])
        feature._id = d['_id']
        return feature

    def db_entry(self):
        entry = {"name": self.name, "ident": self.ident, "attributes": self.attributes}
        if self._id: entry.update({"_id": self._id})
        return entry

    def distance_to(self, other, ranges):
        res = 0.0
        for key in self:
            if isinstance(self[key], str):
                pass
            if type(self[key]) is not type(other[key]):
                raise TypeError
            else: 
                min = ranges[key][0]
                max = ranges[key][1]

                first = self[key]
                second = other[key]

                isdatetime = False

                if isinstance(self[key], datetime.datetime):
                    first = time.mktime(first.timetuple())
                    second = time.mktime(second.timetuple())
                    min = time.mktime(min.timetuple())
                    max = time.mktime(max.timetuple())
                    isdatetime = True

                diff = abs(second - first)
                range = max - min

                if range != 0:
                    res += diff / range / len(self)
        return res

    def merge(self, other):
        new_count = len(self) + len(other)
        for key in self: # iterate over attributes
            if isinstance(self[key], datetime.datetime):
                print "self[key]: %s, other[key]: %s, identsize: %s" % (self[key], other[key], len(other.ident))
                self[key] = datetime.datetime.fromtimestamp(time.mktime(self[key].timetuple()) * len(self) / new_count + time.mktime(other[key].timetuple()) * len(other) / new_count)
            else:
                self[key] = self[key]*len(self)/new_count + other[key]*len(other)/new_count

        self.ident += other.ident

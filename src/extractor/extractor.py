import logging
from collections import defaultdict

from masks import get_all_masks


class ExtractionIterator(object):
    data_iter = iter(list())

    def __init__(self, extractor, data_filehandle=None, data_dict=None):
        self.extractor = extractor
        if data_filehandle is not None and data_dict is None:
            self.data_iter = data_filehandle
        elif data_filehandle is None and data_dict is not None:
            self.data_iter = data_dict.itervalues()
        else:
            raise Exception("Please give dict xor filehandle")
        self.data_iter = extractor.from_filehandle(data_filehandle)

    def next(self):
        for i, d in self.data_iter:
            return self.extractor.extract_dataset(identification=i, data=d)
        else:
            raise StopIteration


class Extractor(object):
    """basic extractor skeletton"""
    available_masks = list()

    def add_feature_mask(self, feature_mask):
        """adds a feature mask to it's collection"""
        self.available_masks.append(feature_mask)

    def add_feature_masks(self, feature_masks):
        """adds a list of feature masks to it's collection"""
        self.available_masks += feature_masks

    def add_all_feature_masks(self, mask_package_names, plug_dir):
        """adds all masks using a whitelist of mask package names"""
        all_masks = get_all_masks(whitelist=mask_package_names, directory=plug_dir)
        self.add_feature_masks(all_masks)

    def extract_dataset(self, ident, data):
        return list()

    def extract(self, data_dict):
        """extraction dummy (returns empty list)"""
        features = defaultdict(list)
        ident = {"name": data_dict["name"], "crawler name": data_dict["crawlerName"],}
        for i, d in data_dict.items():
            features[i] += self.extract_dataset(ident, data_dict["data"])
        return dict(features)

    def from_filehandle(self, filehandle, iterable=False):
        """read data from python filehandle.
        Intended to be used with return value
        from API_crawler.pullDataSet()."""
        import datetime  # eval will use it
        data = dict()
        try:
            data = eval("".join(filehandle.readlines()))  # TODO totally insecure
        except Exception, e:
            logging.error("%s. filehandle: %s", e.message, filehandle)
        return self.extract(data_dict=data)

    def from_file(self, filename, iterable):
        """read data from python file"""
        return self.from_filehandle(filehandle=open(filename, "r"))

    def __repr__(self):
        return "<Extractor masks=%s>" % \
               (str(self.available_masks),)


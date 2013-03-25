#!/usr/bin/env python

"""Extactor module

(c) Peter Schwede

"""

import logging
from os.path import dirname, join
from itertools import imap, izip
from collections import defaultdict


def max_time_resolution(data):
    """calculate smallest time scale"""
    res = None
    sorted_keys = sorted(data.keys())
    old_date = sorted_keys[-1]
    for date in sorted_keys:
        if res is None:
            res = date - old_date
        else:
            res = min(res, date - old_date)
        old_date = date
    return res


class SimpleExtractor(object):
    """extracts features from datasets"""
    def __init__(self):
        self.__available_masks = list()
        self.__running_masks = list()

    def add_feature_mask(self, feature_mask, feature_group):
        """adds a feature mask to it's collection"""
        self.__available_masks.append({"mask_gen" : feature_mask, "feature_group" : feature_group})

    def __may_start(self, this):
        """returns whether a mask is blocked by other instances"""
        for other in self.__running_masks:
            if other.name == this.name and not this.can_overlay:
                return False
        return True

    def extract(self, data_dict):
        """extracts features from data dictionary"""
        res = defaultdict(list)
        for iden, data in data_dict.items():
            #resolution = max_time_resolution(data)
            #resampled = resample(data, resolution)
            logging.debug("iden: %s", iden)
            sorted_times = sorted(data.keys())
            self.__running_masks = list()
            # iterate over all time, value pairs
            for time, value in izip(sorted_times,
                                    imap(lambda k: data[k], sorted_times)):
                # check whether started masks ended and store them as
                # features
                for mask in self.__running_masks:
                    if mask.end(time, value):
                        self.__running_masks.remove(mask)

                        if not mask.is_stub(time, value):
                            feat = mask.make_feature()
                            res[iden].append(feat)
                    else:
                        # mask probably needs a step callback
                        mask.next(time, value)

                # generate new masks
                for mask_rep in self.__available_masks:
                    new_mask = mask_rep['mask_gen'](feature_group)
                    if self.__may_start(new_mask):
                        if new_mask.start(time, value):
                            self.__running_masks.append(new_mask)
            # add the final masks that are still fulfilled
            for mask in self.__running_masks:
                time, value = sorted_times[-1], data[sorted_times[-1]]
                mask.end(time, value)
                if not mask.is_stub(time, value):
                    feat = mask.make_feature()
                    res[iden].append(feat)
        return dict(res)

    def from_file(self, filename):
        """read data from valid python file"""
        import datetime  # eval will use it
        data = {}
        with open(filename, "r") as data_file:
            data = eval("".join(data_file.readlines()))  # TODO insecurity
        return self.extract(data)

    def from_filehandle(self, filehandle):
        """read data from python filehandle. Intended to be used with return
        value from API_crawler.pullDataSet()."""
        import datetime  # eval will use it
        data = {}
        data = eval("".join(filehandle.readlines()))  # TODO totally insecure
        return self.extract(data)

    def __repr__(self):
        return "<Extractor masks=%s>" % \
               (str(self.__available_masks),)


def __cli_interface():
    """cli interface"""
    import pprint
    import argparse

    import masks

    app = argparse.ArgumentParser(description="Command line interface to \
                                              extractor")
    app.add_argument("datafile", type=str,
                     help="file containing python dict of data")
    app.add_argument("masks", type=str,
                     help="will add all plugin content to extractor's feature \
                     masks")
    app.add_argument("-d", "--debug", action="store_true",
                     help="highest verbose mode")
    args = app.parse_args()
    args.masks = args.masks.split(",")

    fstring = "%(levelname)s %(module)s:%(lineno)s %(funcName)s "\
              + "%(message)s"
    loglvl = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(format=fstring, level=loglvl)

    plug_dir = join(dirname(__file__), "masks")
    all_masks = masks.get_all(plug_dir, whitelist=args.masks)
    if len(all_masks) == 0:
        logging.fatal("No masks found: %s", args.masks)
        return 1

    extr = SimpleExtractor()
    for mask in all_masks:
        extr.add_feature_mask(mask)

    pprint.pprint(extr.from_file(args.datafile))
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(__cli_interface())

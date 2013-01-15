#!/usr/bin/env python

import logging
from itertools import imap, izip


class Extractor(object):
    """extracts features from datasets"""
    def __init__(self):
        self.__available_conditions = list()
        self.__running_conditions = list()

    def add_feature_condition(self, ft):
        """adds a feature condition to it's collection"""
        self.__available_conditions.append(ft)

    def __max_time_resolution(self, data):
        """calculate smallest time scale"""
        res = None
        sorted_keys = sorted(data.keys())
        old_t = sorted_keys[-1]
        for t in sorted_keys:
            if res is None:
                res = t - old_t
            else:
                res = min(res, t - old_t)
            old_t = t
        return res

    def __resample(self, data, resolution):
        """interpolate data with a resolution"""
        res = dict()
        return res

    def __may_start(self, this):
        for other in self.__running_conditions:
            if other.name == this.name and not this.can_overlay:
                return False
        return True

    def extract(self, data_dict):
        """extracts features from data dictionary"""
        res = dict()
        for ID, data in data_dict.items():
            #resolution = self.__max_time_resolution(data)
            #resampled = self.__resample(data, resolution)
            logging.debug("ID: %s", ID)
            sorted_times = sorted(data.keys())
            # iterate over all time, value pairs
            for t, v in izip(sorted_times, imap(lambda k: data[k], sorted_times)):
                # check whether started conditions ended and store them as features
                for cond in self.__running_conditions:
                    if cond.end(t, v):
                        self.__running_conditions.remove(cond)

                        feat = cond.make_feature()
                        try:
                            res[ID].append(feat)
                        except KeyError:
                            res[ID] = [feat]
                    else:
                        # cond probably needs a step callback
                        cond.next(t, v)

                # generate new conditions
                for cond_gen in self.__available_conditions:
                    new_cond = cond_gen()
                    if new_cond.start(t, v) and self.__may_start(new_cond):
                        self.__running_conditions.append(new_cond)
        return res

    def __repr__(self):
        return "<Extractor conditions=%s>" % (str(self.__available_conditions),)


def __main():
    import pprint
    import logging
    import argparse
    import datetime  # eval will use it

    import plugins


    app = argparse.ArgumentParser(description="Command line interface to extractor")
    app.add_argument("datafile", type=str,
                     help="file containing python dict of data")
    app.add_argument("plugins", type=str,
                     help="will add all plugin content to extractor's feature conditions")
    app.add_argument("--debug", action="store_true",
                     help="highest verbose mode")
    args = app.parse_args()
    args.plugins = args.plugins.split(",")

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    all_plugins = plugins.get_all(whitelist=args.plugins)
    if len(all_plugins) == 0:
        logging.fatal("No plugins found: %s" % (args.plugins,))
        return 1

    e = Extractor()
    for cond in all_plugins:
        e.add_feature_condition(cond)
    with open(args.datafile, "r") as f:
        data = eval("".join(f.readlines()))
        pprint.pprint(e.extract(data))
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(__main())

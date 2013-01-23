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


class Extractor(object):
    """extracts features from datasets"""
    def __init__(self):
        self.__available_classifiers = list()
        self.__running_classifiers = list()

    def add_feature_classifier(self, feature_classifier):
        """adds a feature classifier to it's collection"""
        self.__available_classifiers.append(feature_classifier)

    def __may_start(self, this):
        """returns whether a classifier is blocked by other instances"""
        for other in self.__running_classifiers:
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
            self.__running_classifiers = list()
            # iterate over all time, value pairs
            for time, value in izip(sorted_times,
                                    imap(lambda k: data[k], sorted_times)):
                # check whether started classifiers ended and store them as
                # features
                for classifier in self.__running_classifiers:
                    if classifier.end(time, value):
                        self.__running_classifiers.remove(classifier)

                        if not classifier.is_stub(time, value):
                            feat = classifier.make_feature()
                            res[iden].append(feat)
                    else:
                        # classifier probably needs a step callback
                        classifier.next(time, value)

                # generate new classifiers
                for classifier_gen in self.__available_classifiers:
                    new_classifier = classifier_gen()
                    if self.__may_start(new_classifier):
                        if new_classifier.start(time, value):
                            self.__running_classifiers.append(new_classifier)
            # add the final classifiers that are still fulfilled
            for classifier in self.__running_classifiers:
                time, value = sorted_times[-1], data[sorted_times[-1]]
                classifier.end(time, value)
                if not classifier.is_stub(time, value):
                    feat = classifier.make_feature()
                    res[iden].append(feat)
        return dict(res)

    def __repr__(self):
        return "<Extractor classifiers=%s>" % \
               (str(self.__available_classifiers),)


def __cli_interface():
    """cli interface"""
    import pprint
    import argparse
    import datetime  # eval will use it

    import classifiers

    app = argparse.ArgumentParser(description="Command line interface to \
                                              extractor")
    app.add_argument("datafile", type=str,
                     help="file containing python dict of data")
    app.add_argument("classifiers", type=str,
                     help="will add all plugin content to extractor's feature \
                     classifiers")
    app.add_argument("-d", "--debug", action="store_true",
                     help="highest verbose mode")
    args = app.parse_args()
    args.classifiers = args.classifiers.split(",")

    fstring = "%(levelname)-8s %(module)-8s:%(lineno)s %(funcName)-8s %(message)s"
    logging.basicConfig(format=fstring, level=logging.DEBUG if args.debug else logging.INFO)

    all_classifiers = classifiers.get_all(join(dirname(__file__), "classifiers"), whitelist=args.classifiers)
    if len(all_classifiers) == 0:
        logging.fatal("No classifiers found: %s", args.classifiers)
        return 1

    extr = Extractor()
    for classifier in all_classifiers:
        extr.add_feature_classifier(classifier)
    with open(args.datafile, "r") as data_file:
        data = eval("".join(data_file.readlines()))
        pprint.pprint(extr.extract(data))
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(__cli_interface())

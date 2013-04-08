#!/usr/bin/env python

"""Extactor module

(c) Peter Schwede

"""

from extractor import Extractor, ExtractionIterator

import logging
from itertools import imap, izip


class SimpleExtractor(Extractor):
    """extracts features from datasets"""
    def __may_start(self, this):
        """returns whether a mask is blocked by other instances"""
        for other in self.__running_masks:
            if other.name == this.name and not this.can_overlay:
                return False
        return True

    def extract_dataset(self, ident, data):
        res = list()
        logging.debug("id: %s", ident)
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
                        feat = mask.make_feature(ident)
                        res.append(feat)
                else:
                    # mask probably needs a step callback
                    mask.next(time, value)

            # generate new masks
            for mask in self.available_masks:
                new_mask = mask()
                if self.__may_start(new_mask):
                    if new_mask.start(time, value):
                        self.__running_masks.append(new_mask)
        # add the final masks that are still fulfilled
        for mask in self.__running_masks:
            time, value = sorted_times[-1], data[sorted_times[-1]]
            mask.end(time, value)
            if not mask.is_stub(time, value):
                feat = mask.make_feature(ident)
                res.append(feat)
        return res


def __cli_interface():
    """cli interface for unit testing"""
    import pprint
    import argparse

    app = argparse.ArgumentParser(description="Command line interface to \
                                              extractor")
    app.add_argument("datafile", type=str,
                     help="file containing python dict of data")
    app.add_argument("masks", type=str,
                     help="will add all plugin content to extractor's feature \
                          masks")
    app.add_argument("--iterate", "-i", action="store_true",
                     help="use iteration")
    app.add_argument("-d", "--debug", action="store_true",
                     help="highest verbose mode")
    args = app.parse_args()
    args.masks = args.masks.split(",")

    fstring = "%(levelname)s %(module)s:%(lineno)s %(funcName)s "\
              + "%(message)s"
    loglvl = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(format=fstring, level=loglvl)

    extr = SimpleExtractor()
    extr.add_all_feature_masks(args.masks)

    if args.iterate:
        import datetime  # eval will use it
        data = eval("".join(open(args.datafile,"r").readlines()))
        for k in ExtractionIterator(data, extr):
            pprint.pprint(k)
    else:
        pprint.pprint(extr.from_file(args.datafile))
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(__cli_interface())

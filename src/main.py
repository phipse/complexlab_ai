# Purpose:    Create API crawler, feature extractor and summarist and provide
#	        channels between the modules.
#	        Test the behaviour and start the grouper, after some data was
#	        gathered.
#
# TLDR:	    Put it all together.
# ----------------------------------------------------------------------------

import json
import logging
from urllib2 import Request, urlopen, URLError
from argparse import ArgumentParser
from os.path import join, exists, realpath, dirname

from util import Task, parse_arg_range
from crawlers import API_crawler
from extractor import Extractor
from extractor.masks import get_all_masks
from summarist import Summarist
from grouper import Grouper


featureFileList = list()
fileListIterator = iter(featureFileList)


def extractor_stream(featureExtractor, crawlerList):
    """ Stream API data to extractor """
    summ = Summarist()
    for crawler in crawlerList:
        while True:
            try:
                ds = crawler.pullDataSet()
                if ds == -1:
                    logging.debug("All files extracted!")
                    return
                extractResult = featureExtractor.from_filehandle(ds)
            except StopIteration:
                logging.debug("StopIteration caught")
                break
            else:
                summ.process(extractResult.itervalues().next())


def crawl(args, crawler_list):
    for c in crawler_list:
        if args.local_ds_build:
            c.buildDataSetFromFs()
            logging.debug("Built dataset from file storage")
        else:
            logging.debug("Running %s", c)
            c.run()
            logging.debug("Done %s", c)


def extract(args, task, crawler_list):
    # init and start feature extractor
    logging.debug("Extracting")
    feature_extractor = Extractor()

    # FEATURE LIST:
    names = parse_arg_range(args.extraction_masks, type_=str)
    all_masks = get_all_masks(names)
    feature_extractor.add_feature_masks(all_masks)

    for mask in task.masks:
        feature_extractor.add_feature_mask(mask['mask_gen'],
                                           mask['feature_group'])

    # data storage paths
    extractor_stream(feature_extractor, crawler_list)
    logging.debug("done extracting")


def group():
    print "Start grouping"
    groupi = Grouper()
    groupi.run()
    print "Finished grouping"


def __parse_args():
    cli = ArgumentParser(description="""Crawls APIs for data and searches
                                     for correlations.""")
    cli.add_argument("data_dir", type=str, help="directory for data storage")
    cli.add_argument("task_path", type=str, help="path to task.json")
    cli.add_argument("--mongo-url", "-m", default="http://127.0.0.1:27017",
                     help="DO NOT crawl from APIs",)
    cli.add_argument("--skip-crawl", "-c", default=False, action="store_true",
                     help="DO NOT crawl from APIs",)
    cli.add_argument("--local-ds-build", "-l", default=False,
                     action="store_true",
                     help="Build crawler dataset from local data",)
    cli.add_argument("--skip-group", "-g", default=False, action="store_true",
                     help="DO NOT group extracted data",)
    cli.add_argument("--skip-extract", "-e", default=False,
                     action="store_true",
                     help="DO NOT extract from files",)
    cli.add_argument("--extraction_masks", "-x", default="", type=str,
                     help="comma separated list of mask names")
    cli.add_argument("--verbose", "-v", default=0, type=int,
                     help="verbose mode")
    args = cli.parse_args()
    args.src_path = dirname(realpath(__file__))
    args.real_data_dir = realpath(args.data_dir)
    logging.debug(json.dumps(vars(args)))
    return args


def __setup_logging(args):
    lvl = logging.DEBUG if args.verbose > 0 else logging.INFO
    logging.basicConfig(level=lvl)


def __validate_paths(args):
    for p in [args.src_path, args.real_data_dir]:
        if not exists(p):
            logging.fatal("%s does not exist.", p)
            return False
    try:
        urlopen(Request(args.mongo_url))
    except URLError:
        logging.fatal("%s unreachable. MongoDB daemon not running?",
                      args.mongo_url)
        return False
    return True


def __prepare_task(args):
    """prepares the task givein by args.task_path"""
    task_path = args.task_path
    if not task_path.endswith(".json"):
        task_path = join("tasks/", "%s.json" % task_path)
    return Task(task_path)


def __setup_crawlers(args):
    create_crawler = lambda x: API_crawler(join(args.src_path,
                                                "crawlers/%s" % x),
                                           args.real_data_dir)
    crawlers = ["NASDAQ_syms",
                #"NYSE_syms",
                ]
    crawlerList = [create_crawler(c) for c in crawlers]
    logging.debug("Crawler init done")
    return crawlerList


def __cli_main():
    args = __parse_args()
    __setup_logging(args)
    if not __validate_paths(args):
        return 1

    # maybe thread this? up until now, I store results on disk; caching? -- phi
    task, crawler_list = __prepare_task(args), __setup_crawlers(args)

    if not args.skip_crawl:
        crawl(args, crawler_list)
    if not args.skip_extract:
        extract(args, task, crawler_list)
    if not args.skip_group:
        group()

    logging.debug("Everything done.")
    return 0


if __name__ == "__main__":
    __cli_main()

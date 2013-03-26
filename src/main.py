# vim:set ts=2 sw=2:

# Purpose:  Create API crawler, feature extractor and summarist and provide
#	    channels between the modules.
#	    Test the behaviour and start the grouper, after some data was
#	    gathered.
#
# TLDR:	  Put it all together.
# ----------------------------------------------------------------------------

import logging
from urllib2 import Request, urlopen, URLError
from argparse import ArgumentParser
from os import makedirs
from os.path import join, exists, realpath, dirname

from util import Task, parse_arg_range
from crawlers import API_crawler
from extractor import Extractor
from extractor.masks import get_all_masks
from summarist import Summarist
from grouper import Grouper


featureFileList = list()
fileListIterator = iter(featureFileList)


def extractorStream(featureExtractor, crawlerList):
  """ Stream API data to extractor """
  summ = Summarist()
  for crawler in crawlerList:
    while True:
      try:
        ds = crawler.pullDataSet()
        if ds == -1:
          print "All files extracted!"
          return
        extractResult = featureExtractor.from_filehandle(ds)
      except StopIteration:
        print "StopIteration caught"
        break
  else:
    summ.process(extractResult.itervalues().next())


def startGrouping():
  print "Start grouping"
  groupi = Grouper()
  groupi.run()
  print "Finished grouping"


def __cli_main():
  app = ArgumentParser(description="""Crawls APIs for data and searches\
                                   for correlations.""")
  app.add_argument("data_dir", type=str, help="directory for data storage")
  app.add_argument("task_path", type=str, help="path to task.json")
  app.add_argument("--skip-crawl", "-c", default=False, action="store_false",
                   help="DO NOT crawl from APIs",)
  app.add_argument("--skip-group", "-g", default=False, action="store_false",
                   help="DO NOT group extracted data",)
  app.add_argument("--skip-extract", "-e", default=False, action="store_false",
                   help="DO NOT extract from files",)
  app.add_argument("--extraction_masks", "-m", default="", type=str,
                   help="comma separated list of mask names")
  app.add_argument("--verbose", "-v", default=0, type=int,
                   help="verbose mode")
  args = app.parse_args()

  logging.basicConfig(level=logging.DEBUG if args.verbose > 0
                                          else logging.INFO)

  SRCPATH = dirname(realpath(__file__))
  DATAPATH = realpath(args.data_dir)
  EXTRPATH = join(args.data_dir, "extraction/")
  MONGOSERV = "127.0.0.1"
  MONGOPORT = 27017
  MONGOURL = "http://%s:%i" % (MONGOSERV, MONGOPORT,)

  # parse task
  TASKPATH = args.task_path
  if not TASKPATH.endswith(".json"):
    TASKPATH = join("tasks/", "%s.json" % TASKPATH)
  task = Task(TASKPATH)

  assert exists(SRCPATH)
  assert exists(DATAPATH)
  assert exists(TASKPATH)
  if not exists(EXTRPATH):
    makedirs(EXTRPATH)
  assert exists(EXTRPATH)

  try:
    urlopen(Request(MONGOURL))
  except URLError:
    logging.fatal("MongoDB daemon not running?")
    return 1

  if not args.skip_crawl:
    create_crawler = lambda x: API_crawler(join(SRCPATH,
                                                "crawlers/%s" % x),
                                           DATAPATH)

    crawlers = ["NASDAQ_syms",
                #"NYSE_syms",
               ]
    crawlerList = [create_crawler(c) for c in crawlers]

    logging.debug("Crawler init done")

    # maybe thread this? up until now, I store results on disk; caching? -- phi

    # if you have a dataset in this directory use this, else aquire a new one
    # by running the crawler --phi

    for c in crawlerList:
      c.buildDataSetFromFs()
      logging.debug("Built dataset from file storage")
      logging.debug("Running %s", c)
      c.run()
      logging.debug("Done %s", c)

  if not args.skip_extract:
    # init and start feature extractor
    logging.debug("Extracting")
    featureExtractor = Extractor()

    # FEATURE LIST:
    all_masks = get_all_masks(parse_arg_range(args.extraction_masks, type_=str))
    featureExtractor.add_feature_masks(all_masks)

    for mask in task.masks:
      featureExtractor.add_feature_mask(mask['mask_gen'], mask['feature_group'])

    # data storage paths
    extractorStream(featureExtractor, crawlerList)
    logging.debug("done extracting")
  
  if not args.skip_group:
    logging.debug("starting to group")
    startGrouping()

  logging.debug("Everything done.")
  return 0


if __name__ == "__main__":
  __cli_main()

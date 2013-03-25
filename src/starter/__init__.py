# Purpose:  Create API crawler, feature extractor and summarist and provide
#	    channels between the modules.
#	    Test the behaviour and start the grouper, after some data was
#	    gathered.
#
# TLDR:	  Put it all together.
# ----------------------------------------------------------------------------

from crawlers import API_crawler
from extractor import Extractor
from extractor.masks import get_all_masks
from summarist import Summarist
from grouper import Grouper
from os import path, makedirs, remove
import sys


featureFileList = list()
fileListIterator = iter(featureFileList)

def extractorStream( extractDataPath, crawlerList ):
  """ Stream API data to extractor """
  summ = Summarist()
  for crawler in crawlerList:
    while True:
      try:
	ds = crawler.pullDataSet()
	if ds == -1:
	  print "All files extracted!"
	  return
        extractResult = featureExtractor.from_filehandle( ds )
      except StopIteration:
	print "StopIteration caught" 
	break
      else:
	summ.process( extractResult.itervalues().next() )
	"""
	# store extractResult in fs
	extFileName = str(extractResult.keys())
	extFileName = extFileName[2:len(extFileName)-2]
	extFileName = extractDataPath + extFileName;
	#print extFileName 
	if not path.exists(extractDataPath):
	  makedirs(extractDataPath) 
	if path.isfile(extFileName):
	  remove(extFileName)
	f = file( extFileName, "w+" )
	f.write( str(extractResult) )
	featureFileList.append( extFileName )
	f.flush()
	f.close()
"""


def startGrouping():
  print "Start grouping"
  groupi = Grouper()
  groupi.run()
  print "Finished grouping"



if __name__ == "__main__":
  ROOTSRCPATH = sys.argv[1] + "/"; # passed in src/start
  print "root src path: " + ROOTSRCPATH
  ROOTDATAPATH = ROOTSRCPATH + "../data/"

  if False:
    nasdaqCrawler = API_crawler( ROOTSRCPATH + "crawlers/NASDAQ_syms", ROOTDATAPATH )
    nyseCrawler = API_crawler( ROOTSRCPATH + "crawlers/NYSE_syms", ROOTDATAPATH )
    crawlerList = list()
    crawlerList.append(nasdaqCrawler)
    #crawlerList.append(nyseCrawler)
    print "crawler init done"


  # maybe thread this? up until now, I store results on disk; caching? -- phi
  # if you have a dataset in this directory use this, else aquire a new one by
  # running the crawler --phi
    nasdaqCrawler.buildDataSetFromFs()
    #nasdaqCrawler.run()
    #nyseCrawler.run()

# init and start feature extractor
    featureExtractor = Extractor()

# FEATURE LIST:
    #featureExtractor.add_feature_masks(get_all_masks(["monotony"]))
    #featureExtractor.add_feature_masks(get_all_masks(["relative_monotony"]))
    featureExtractor.add_feature_masks(get_all_masks(["absolute_monotony"]))

# data storage paths
    extractDataPath = ROOTDATAPATH + "extraction/"
    extractorStream( extractDataPath, crawlerList )
    startGrouping()
  else:
    startGrouping()

  print "done"

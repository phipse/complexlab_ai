# Purpose:  Create API crawler, feature extractor and summarist and provide
#	    channels between the modules.
#	    Test the behaviour and start the grouper, after some data was
#	    gathered.
#
# TLDR:	  Put it all together.
# ----------------------------------------------------------------------------

from crawlers import API_crawler
from extractor import Extractor
from extractor.masks import absolute_monotony
from extractor.masks import relative_monotony
from summarist import Summarist
from os import path, makedirs, remove


featureFileList = list()
fileListIterator = iter(featureFileList)

def extractorStream( extractDataPath, crawlerList ):
  """ Stream API data to extractor """
  summ = Summarist()
  for crawler in crawlerList:
    while True:
      try:
        extractResult = featureExtractor.from_filehandle( crawler.pullDataSet() )
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




if __name__ == "__main__":
  nasdaqCrawler = API_crawler( "crawlers/NASDAQ_syms" )
  nyseCrawler = API_crawler( "crawlers/NYSE_syms" )
  crawlerList = list()
  crawlerList.append(nasdaqCrawler)
  crawlerList.append(nyseCrawler)
  print "crawler init done"

  
  # maybe thread this? up until now, I store results on disk; caching? -- phi
  # if you have a dataset in this directory use this, else aquire a new one by
  # running the crawler --phi
  #fsPath = "../../data/dicts/"
  #nasdaqCrawler.buildDataSetFromFs(fsPath)
  nasdaqCrawler.run()
  #nyseCrawler.run()

# init and start feature extractor
  featureExtractor = Extractor()

# FEATURE LIST:
  #featureExtractor.add_feature_mask(monotony.Increasing)
  #featureExtractor.add_feature_mask(monotony.Decreasing)
  featureExtractor.add_feature_mask(absolute_monotony.AbsoluteIncreasing)
  featureExtractor.add_feature_mask(absolute_monotony.AbsoluteDecreasing)
  #featureExtractor.add_feature_mask(relative_monotony.RelativeIncreasing)
  #featureExtractor.add_feature_mask(relative_monotony.RelativeDecreasing)

# data storage paths
  extractDataPath = "../data/extraction/"
  extractorStream( extractDataPath, crawlerList )

  print "done"

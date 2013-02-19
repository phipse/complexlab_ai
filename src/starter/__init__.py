# Purpose:  Create API crawler, feature extractor and summarist and provide
#	    channels between the modules.
#	    Test the behaviour and start the grouper, after some data was
#	    gathered.
#
# TLDR:	  Put it all together.
# ----------------------------------------------------------------------------

from crawlers import API_crawler
from extractor import Extractor
from classifiers import monotony
from classifiers import absolute_monotony
from classifiers import relative_monotony
from os import path, makedirs, remove


def extractorStream( extractDataPath, crawlerList ):
  """ Stream API data to extractor """
  for crawler in crawlerList:
    while True:
      try:
        extractResult = featureExtractor.from_filehandle( crawler.pullDataSet() )
      except StopIteration:
	print "StopIteration caught" 
	break
      else:
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
	f.flush()
	f.close()





if __name__ == "__main__":
  nasdaqCrawler = API_crawler( "../crawlers/NASDAQ_syms" )
  nyseCrawler = API_crawler( "../crawlers/NYSE_syms" )
  crawlerList = list()
  crawlerList.append(nasdaqCrawler)
  crawlerList.append(nyseCrawler)
  print "crawler init done"

  
  # maybe thread this? up until now, I store results on disk; caching? -- phi
  nasdaqCrawler.run()
  nyseCrawler.run()


# init and start feature extractor
  featureExtractor = Extractor()

# FEATURE LIST:

  #featureExtractor.add_feature_classifier(monotony.Increasing)
  #featureExtractor.add_feature_classifier(monotony.Decreasing)
  featureExtractor.add_feature_classifier(absolute_monotony.AbsoluteIncreasing)
  featureExtractor.add_feature_classifier(absolute_monotony.AbsoluteDecreasing)
  #featureExtractor.add_feature_classifier(relative_monotony.RelativeIncreasing)
  #featureExtractor.add_feature_classifier(relative_monotony.RelativeDecreasing)

# data storage paths
  extractDataPath = "../../data/extraction/"
  extractorStream( extractDataPath, crawlerList )

  print "done"

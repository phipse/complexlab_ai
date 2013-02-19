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

if __name__ == "__main__":
  nasdaqCrawler = API_crawler( "../crawlers/NASDAQ_syms" )
  nyseCrawler = API_crawler( "../crawlers/NYSE_syms" )
  crawlerList = list()
  crawlerList.append(nasdaqCrawler)
  crawlerList.append(nyseCrawler)
  print "craweler init done"

  
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

# API-Data-Stream to extractor
  for crawler in crawlerList:
    while True:
      try:
        extractResult = featureExtractor.from_filehandle( crawler.pullDataSet() )
      except StopIteration:
	print "StopIteration caught" 
	break
      else:
	# store extractResult in fs
	print extractResult


  print "done"

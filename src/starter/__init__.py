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
  lseCrawler = API_crawler( "../crawlers/LSE_syms" )

  print "craweler init done"

  
  # maybe thread this? up until now, I store results on disk; caching? -- phi
  nasdaqCrawler.run()
#  nyseCrawler.run()
#  lseCrawler.run()


  # init and start feature extractor

  featureExtractor = Extractor()
#  featureExtractor.add_feature_classifier(monotony.Increasing)
#  featureExtractor.add_feature_classifier(monotony.Decreasing)
  featureExtractor.add_feature_classifier(absolute_monotony.AbsoluteIncreasing)
  featureExtractor.add_feature_classifier(absolute_monotony.AbsoluteDecreasing)
#  featureExtractor.add_feature_classifier(relative_monotony.RelativeIncreasing)
#  featureExtractor.add_feature_classifier(relative_monotony.RelativeDecreasing)

  while True:
    try:
      extractResult = featureExtractor.from_filehandle( nasdaqCrawler.pullDataSet() )
    except StopIteration:
      print "StopIteration caught" 
      break
    print extractResult

  print "done"

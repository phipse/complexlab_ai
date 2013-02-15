# Purpose:  Create API crawler, feature extractor and summarist and provide
#	    channels between the modules.
#	    Test the behaviour and start the grouper, after some data was
#	    gathered.
#
# TLDR:	  Put it all together.
# ----------------------------------------------------------------------------

from crawlers import API_crawler
from extractor import Extractor 

if __name__ == "__main__":
  nasdaqCrawler = API_crawler( "../crawlers/NASDAQ_syms" )
  nyseCrawler = API_crawler( "../crawlers/NYSE_syms" )
  lseCrawler = API_crawler( "../crawlers/LSE_syms" )

  print "craweler init done"

  
  # maybe thread this? up until now, I store results on disk; caching? -- phi
  nasdaqCrawler.run()
  nyseCrawler.run()
  lseCrawler.run()


  # init and start feature extractor

#  featureExtractor = Extractor(



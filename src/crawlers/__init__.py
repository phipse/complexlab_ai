import logging
from datetime import date
from os.path import isfile, exists, join
import os
import tempfile 
import requests
import json
from multiprocessing import Process, Queue

class API_crawler(object):

  def __init__(self, syms, dataPath, startTime): 
    self.__index = 0
    self.__identifier = list()  
    self.__first = True
    self.__requestAddresses = list()
    self.__fileNames = list()
    self.__fileIterator = iter(self.__fileNames)
    self.__symfile = file( syms, "r" )
    if startTime != None:
        self.__crawlStartTime = startTime
    else:
        self.__crawlStartTime=1900
    self.initIdentifier()
    self._dataPath = dataPath
    self.crawlerName = syms.split('/')[len(syms.split('/'))-1].split('_')[0]
 

  def initIdentifier(self):
    if self.__first:
      for line in self.__symfile.readlines():
	self.__identifier.append(line.split("\n")[0])
      self.__first = False


  def setTimeFrame(self):
    today = date.today()
    startString = "&a=0&b=1&c=" + str(self.__crawlStartTime) + "&d=%i&e=%i&f=%i"
    return startString % (today.month-1, today.day, today.year,)


  def setID(self):
    ret = self.__identifier[self.__index]
    self.__index = self.__index+1
    if self.__index > len(self.__identifier):
      self.__index = 0
    return ret


  def run(self):
    startString = "http://ichart.finance.yahoo.com/table.csv?"
    for x in range(len(self.__identifier)):
      buildString = startString + "s=" + self.setID();
      buildString += self.setTimeFrame()
      self.__requestAddresses.append(buildString)
    
    addressLen = len(self.__requestAddresses)
    three = addressLen/3
    
    # three processes
    a = self.__requestAddresses[0:three]
    b = self.__requestAddresses[three:three+three]
    c = self.__requestAddresses[three+three:addressLen-1]
    #three queues
    aq = Queue(10)
    bq = Queue(10)
    cq = Queue(10)

    a = Process(target=self.requestCSV, args=(aq, a,))
    b = Process(target=self.requestCSV, args=(bq, b,))
    c = Process(target=self.requestCSV, args=(cq, c,))
    a.start()
    b.start()
    c.start()
    #empty each queue before joining
    lastA = aq.get()
    lastB = bq.get()
    lastC = cq.get()
    # "close" is a sentinel value
    while( True ):
      if lastA != "close":
	self.__fileNames.append(lastA)
	lastA = aq.get()
      if lastB != "close":
	self.__fileNames.append(lastB)
	lastB = bq.get()
      if lastC != "close":
	self.__fileNames.append(lastC)
	lastC = cq.get()
      if lastA == "close" and lastB == "close" and lastC == "close":
	break;

    a.join()
    b.join()
    c.join()

  
  
  def requestCSV(self, queue, requestAddresses):
    cnt = 0
    for symbol in requestAddresses:
      r = requests.get(symbol)
      if r.status_code != 200: continue
      logging.debug("symbol: " + symbol)
      logging.debug("status: %s", r.status_code)
      storepath = join(self._dataPath, "dicts/") #"../../data/dicts/"
      
      test = tempfile.TemporaryFile()
      test.write(r.text)
      test.flush()
      test.seek(0)
      test.readline() #discard description
      dictusMongus = dict()

      for line in test.readlines():
		line = line.split(",")
		dat = line[0]
		value = float(line[4])
		dat = dat.split("-")
		ti = date( int(dat[0]), int(dat[1]), int(dat[2]) )
		dictusMongus.update( {ti:value} )
      
      identStart = symbol.find("s=")
      identEnd = symbol.find("&a")
      identName = symbol[identStart+2:identEnd]


      nojs = { 'crawlerName' : self.crawlerName }
      nojs.update({ 'name' : identName })
      nojs.update({ 'data' : dictusMongus})
      filename = join(storepath, identName)
      if not exists(storepath):
		os.makedirs(storepath) 
      if isfile(filename):
		os.remove(filename)
      f = file(filename, "w+")
      f.write( str( nojs))
      f.flush()
      # append new file to the list of all filenames
      # as this is now multiprocessed put the filename in the queue
      queue.put(filename)
      f.close()
      cnt += 1
      # STOP CRAWLING AFTER cnt FILES:
      if cnt == 3:
		break;
    queue.put("close")
    queue.close()
    logging.debug( "done" )

  
  def pullDataSet(self):
    try:
      ret = self.__fileIterator.next()
    except StopIteration:
      return -1;
    else:
      return file( ret, "r" )


  def buildDataSetFromFs(self):
    logging.debug("Building dataset from local files")
    dataSetPath = join(self._dataPath, "dicts/")
    if not exists(dataSetPath):
      return -1;

    for i in range(len(self.__identifier)):
      if i > 10:
	break
      sym = join(dataSetPath, self.__identifier[i])
      if isfile(sym):
	self.__fileNames.append(sym)
      else:
	break
    
    logging.debug("Building done")
    

  def getCrawlerName(self):
	  return self.crawlerName

if __name__ == "__main__":
  crawl = API_crawler( "NASDAQ_syms", "../../data/dicts/", None )
  crawl.run()
  #for i in range(10):
  #  crawl.pullDataSet()


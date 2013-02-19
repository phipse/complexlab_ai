from datetime import date
from os import path
import os
import tempfile 
import requests
import json

class API_crawler(object):

  def __init__(self, syms): 
    self.__index = 0
    self.__identifier = list()  
    self.__first = True
    self.__requestAddresses = list()
    self.__fileNames = list()
    self.__fileIterator = iter(self.__fileNames)
    self.__symfile = file( syms, "r" )
    self.initIdentifier()
 

  def initIdentifier(self):
    if self.__first:
      for line in self.__symfile.readlines():
	self.__identifier.append(line.split("\n")[0])
      self.__first = False


  def setTimeFrame(self):
    startString = "&a=0&b=1&c=1900"
    today = date.today()
    pieces = str(today).split("-")
    startString += "&d="+ str( int(pieces[1])-1 );
    startString += "&e=" + str( int( pieces[2] ) );
    startString += "&f=" + str( int( pieces[0] ) );
    return startString


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
    print len(self.__requestAddresses)
    self.requestCSV()

  
  
  def requestCSV(self):
    cnt = 0
    for symbol in self.__requestAddresses:
      r = requests.get(symbol)
      if r.status_code != int(200): continue
      print "symbol: " + symbol 
      print "status: " + str(r.status_code)
      storepath = "../../data/dicts/"
    
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

      nojs = { self.__identifier[cnt] : dictusMongus}
      filename = storepath + self.__identifier[cnt]
      if not path.exists(storepath):
	os.makedirs(storepath) 
      if path.isfile(filename):
	os.remove(filename)
      f = file(filename, "w+")
      f.write( str( nojs))
      f.flush()
      # append new file to the list of all filenames
      self.__fileNames.append(filename)
      f.close()
      cnt += 1
      if cnt == 10:
	break
    print "done"

  
  def pullDataSet(self):
    return file( self.__fileIterator.next(), "r" )
    






if __name__ == "__main__":
  crawl = API_crawler( "NASDAQ_syms" )
  crawl.run()
  for i in range(10):
    crawl.pullDataSet()


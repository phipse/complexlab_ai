from datetime import date
from os import path
import os
import tempfile 
import requests
import json

class API_crawler:
  index = 0
  identifier = list()  
  first = True
  requestAddresses = list()
  fileNames = list()
  fileIterator = iter(fileNames)

  def __init__(self, syms): 
    self.symfile = file( syms, "r" )
    self.initIdentifier()
 

  def initIdentifier(self):
    if self.first:
      for line in self.symfile.readlines():
	self.identifier.append(line.split("\n")[0])
      self.first = False


  def setTimeFrame(self):
    startString = "&a=0&b=1&c=1900"
    today = date.today()
    pieces = str(today).split("-")
    startString += "&d="+ str( int(pieces[1])-1 );
    startString += "&e=" + str( int( pieces[2] ) );
    startString += "&f=" + str( int( pieces[0] ) );
    return startString


  def setID(self):
    ret = self.identifier[self.index]
    self.index = self.index+1
    if self.index > len(self.identifier):
      self.index = 0
    return ret


  def run(self):
    startString = "http://ichart.finance.yahoo.com/table.csv?"
    for x in range(len(self.identifier)):
      buildString = startString + "s=" + self.setID();
      buildString += self.setTimeFrame()
      self.requestAddresses.append(buildString)
#    print len(self.requestAddresses)
    self.requestCSV()

  
  
  def requestCSV(self):
    cnt = 0
    for symbol in self.requestAddresses:
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

      nojs = { self.identifier[cnt] : dictusMongus}
      filename = storepath + self.identifier[cnt]
      if not path.exists(storepath):
	os.makedirs(storepath) 
      if path.isfile(filename):
	os.remove(filename)
      f = file(filename, "w+")
      f.write( str( nojs))
      f.flush()
      # append new file to the list of all filenames
      self.fileNames.append(filename)
      f.close()
      cnt += 1
      if cnt == 10:
	break
    print "done"

  
  def pullDataSet(self):
    return file( self.fileIterator.next(), "r" )
    






if __name__ == "__main__":
  crawl = API_crawler( "NASDAQ_syms" )
  crawl.run()
  for i in range(10):
    crawl.pullDataSet()


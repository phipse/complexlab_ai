from datetime import date
from os import path
import requests
import json

class API_crawler:
  index = 0
  identifier = list()  
  first = True
  requestAddresses = list()

  def __init__(self): 
    self.initIdentifier()
 

  def initIdentifier(self):
    if self.first:
      symfile = file("NASDAQ_syms", "r")
      for line in symfile.readlines():
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
    self.parseTimeClose()
  
  
  def requestCSV(self):
    r = requests.get(self.requestAddresses[0])
    test = file( "response", "a" )
    test.write(r.text)
    test.flush()
    test.close()
    test = file( "response", "rw")
    out = file( "result", "a")
    for line in test.readlines():
      line = line.split(",")
      str = line[0] + "," + line[4] + "\n" 
      out.write(str)
      
  def parseTimeClose(self):
    f = file( "result", "r")
    g = file( "times" , "a")
    f.readline() # discard description line
    li = f.readline()
    datVal = li.split(",")
    dat = datVal[0].split("-")
    val = datVal[1].split("\n")[0]
    ti = date( int(dat[0]), int(dat[1]), int(dat[2]) )
    nojs = { self.identifier[0]: {ti: val}}
    
    print ti
    print val
    print nojs






if __name__ == "__main__":
  crawl = API_crawler()
  crawl.run()

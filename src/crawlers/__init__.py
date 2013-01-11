from datetime import date
from os import path

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



if __name__ == "__main__":
  crawl = API_crawler()
  crawl.run()

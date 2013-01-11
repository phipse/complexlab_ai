from datetime import date

class API_crawler:
  index = 0
  

  def setTimeFrame(self):
    startString = "&a=0&b=1&c=1900"
    today = date.today()
    pieces = str(today).split("-")
#    print pieces
    startString += "&d="+ str( int(pieces[1])-1 );
    startString += "&e=" + str( int( pieces[2] ) );
    startString += "&f=" + str( int( pieces[0] ) );
    return startString
#    print startString

  def setID(self):
#    identifier = list(iterable)
#    ret = identifier(self.index)
#    self.index = self.index+1
    ret = "s=GOOG"
    return ret

  def run(self):
    startString = "http://ichart.finance.yahoo.com/table.csv?"
    startString += self.setID();
    startString += self.setTimeFrame()
    print startString

if __name__ == "__main__":
  crawl = API_crawler()
  crawl.run()

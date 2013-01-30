#!/bin/python

from pymongo import MongoClient

class Grouper:
  first = True
  db
  charactDB

  def init(self):
    connection = MongoClient()
    self.db = connection.ai
    # open db connection, read collection and copy it
    for x in self.db.Characteristics.find():
      self.charactDB.insert(x)
  
  def grouping(self):
# databsae layout:
#   Characteristic: ID,{ID}

  # Options:
  # 1. generate ID: {Characteristic} - table and check for equal characts
  # 2. build charact-set for first ID, check own characteristics for equal
    # IDs and save (non-)equality in a matrix
  # 3. gerate all Characteristic combinations and intersect their ID-Sets
      # delete empty characteristic combinations?
      # -> approach is complete
      # -> works directly on database layout
      # -> simple

#  ---------------------------
# mongo shit
    for x in list(10):
      max_element = x;
      charactDB = charactDB.map_reduce( self.mapfunc(max_element),
	  slef.reducefunc(), self.intersect() );

  # for each char1 in db which has one_element
  #   for each char2 in db which has max_elements
  #	create new char1_charMax and intersect char1.val charMax.val
  # repeat until max_elements == Maximum one element characteristics
  
#  for x in charSet:
#    if len(x) == 1:
#      for y in charSet2:
#	if len(x) == max_element:
#	  newUnionSet = union( x, y)
#	  x_val = self.db.


  def mapfunc(self, maxChar):
    # mongodb wants javascript for map reduce
    # checks: don't join me with myself; 
    #	      if I am a joined ID, ignore me unless I am a max size concatenation;
    #	      if the ID you want to join me with, is already joined, ignore it;
    return """ function( maxChar ) {
      self = this;
      if( self.split('_').length < maxChar ) return;
      this._id.forEach( function( x ) {
	if( self._id == x ) return;
	if( x.split('_').length > 1 ) return;
	emit( [self._id, id].sort().join('_'), self.value );
      }
    }; """

  def reducefunc(self):
    return """ function( key, values ) {
      return value : intersect( null, values );
      }
      """


  def intesect(self):
    return """intersectFunc = function( a, b ) {
		a.filter( function(x) { return b.indexOf(x) >= 0; ) });
	      }"""
  
  
#  def cleanup(self):
    # if group has not enough members 
    #	mark as uninteresting

  def run(self):
    if first: 
      init()
      first = False
    grouping()





if __name__ == "__main__":
  grouper = Grouper()
  grouper.run()
  

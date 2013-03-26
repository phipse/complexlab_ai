#!/bin/python

from pymongo import Connection

class Grouper(object):
  
  def __init__(self):
  # open db connection, read collection and copy it
    connection = Connection()
    self.__db = connection.ai
    self.__charactDB = self.__db.features
    for x in self.__db.Characteristics.find():
      self.__charactDB.insert(x)
  
  def grouping(self):
# database layout:
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
    IDs = self.__charactDB.distinct('name')
    for max_element in range(10):
      self.__charactDB = self.__charactDB.map_reduce( self.mapfunc(max_element),
      self.reducefunc(),{ "reduce": "charactGroups" },
      scope= { "ids": IDs } ); 

  # for each char1 in db which has one_element
  #   for each char2 in db which has max_elements
  #	create new char1_charMax and intersect char1.val charMax.val
  # repeat until max_elements == Maximum one element characteristics


  def mapfunc(self, maxChar):
    # mongodb wants javascript for map reduce
    # checks: don't join me with myself; 
    #	      if I am a joined ID, ignore me unless I am a max size concatenation;
    #	      if the ID you want to join me with, is already joined, ignore it;
    #	      if I already contain the ID you want to join me with, ignore it;
    #
    # BUGS: somehow the grouper creates DB_entries with the name in the _id
    # section, I guess its a mongodb internal thing. 
    #	I think it's the grouper, as the summarist is not writing to _id
    # ERROR: Cannot wirte property name to read-only object
    #	Where the fuck is that coming frome? 
    return """function map( maxChar ) {
      self = this;
      if( self.name == undefined )
      {	
        if( self._id != undefined ) 
	{
	  self.name = self._id;
	}
	else
	{
	  print( "self _id: " + self._id );
	  print( "self object_id: " + self._object_id );
	}
      }
      if( self.name.split('_').length < maxChar ) return;
      ids.forEach( function( x ) {
	if( self.name == x ) return;
	if( x.split('_').length > 1 ) return;
	if( self.name.split('_').indexOf(x) != -1 ) return;
	emit( [self.name, x].sort().join('_'), self.attributes );
      })
    }; """

  def reducefunc(self):
    return """function reduce( key, values ) {
	print(key)
	print(values)
      };
      """


  def intersect(self):
    return """intersect = function( a, b ) {
		a.filter( function(x) { return b.indexOf(x) >= 0; });
	      };"""
  
  
#  def cleanup(self):
    # if group has not enough members 
    #	mark as uninteresting

  def run(self):
    self.grouping()





if __name__ == "__main__":
  grouper = Grouper()
  grouper.run()
  

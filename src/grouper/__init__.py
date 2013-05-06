#!/bin/python

from pymongo import Connection
import logging

class Grouper(object):
  
    def __init__(self):
        # open db connection, read collection and copy it
        connection = Connection()
        self.__db = connection.ai
        self.__characTable = self.__db.characteristics
        self.identDbSetup()
#        self.__charactDB = self.__db.charactDB
#        for x in self.__db.Characteristics.find():
#            self.__charactDB.insert(x)



    def identDbSetup(self):
        '''Insert elements in the form of { Identifier : [characteristics] } to
        a new collection'''
        
        logging.debug( "Setup ident database." )
        idDb = self.__db.idents
        if idDb.find().count() > 0:
            return;
        for ele in self.__characTable.find():
            for ident in ele['ident']:
                key = ident['crawler name'] + "/" + ident['name']
                value = ele['_id'] 
                # if identifier already in the DB, update the value aka
                # characteristics list
                cursor = idDb.find( {'name' : key })
                if cursor.count() > 0:
                    for oldEntry in cursor:
                        valueList = oldEntry['value']
                        valueList.append(value)
                        idDb.update( {'name' : key }, { "$set" : { "value" : \
                            valueList } } )
                else:
                    idDb.insert( {'name': key, 'value': [value]} )
        logging.debug("New database setup: idents")



    def combineIdents(self): 
        '''Combines two entries and intersects the characteristic lists'''

        logging.debug( "Grouping via combineIdents" )
        idDb = self.__db.idents
        combIdDb = self.__db.combIds
        for x in range(1,5):
            for ele in idDb.find():
                for snd in idDb.find():
                    if ele == snd:
                        continue;
                    if not self.namePartial( ele['name'], snd['name'] ):
                        newKey = "_".join( sorted( set( \
                            sorted( (ele['name']).split('_') ) + \
                            sorted( (snd['name']).split('_') )  ) ) )
                        newValue = self.intersect( ele['value'], snd['value'] )
                        toInsert = {'name' : newKey, 'value' : newValue}
                        if len(newValue) != 0:
                            if idDb.find( toInsert ).count() == 0:
                                idDb.insert( toInsert  )
                                logging.debug( "Combined Ident inserted: %s", \
                                        toInsert )
                    

    def namePartial(self, fst, snd):
        '''Tests if parts of the second name are already present in the first
        name. If so returns True, if not return False.'''
        fst = fst.split('_')
        snd = snd.split('_')
        for x in snd:
            if x in fst:
                return True
        return False


    def intersect(self, first, second):
        '''Intersects two lists of elements. Be aware, that lists lose
        duplicated items.'''
        return list( set(first).intersection(set(second)) )



      # database layout:
#   Characteristic: ID,{ID}

  # Options:
  # 1. generate ID: [Characteristic] - table and check for equal characts
  # 2. build charact-set for first ID, check own characteristics for equal
    # IDs and save (non-)equality in a matrix
  # 3. gerate all Characteristic combinations and intersect their ID-Sets
      # delete empty characteristic combinations?
      # -> approach is complete
      # -> works directly on database layout
      # -> simple

#  ---------------------------
# mongo shit
    def grouping(self):
        ''' On basis of the db.idents collection map reduce is executed to generate
        all combinations '''
        # idDbSetup done; "_id", "name", "value"
        
        logging.debug( "Grouping via MapReduce" );
        IDs = self.__db.idents.distinct('name')
        ret =  self.__db.idents.map_reduce( \
                self.mapfunc(), \
                self.reducefunc(), \
                "reduced", \
                scope= { "ids": IDs, "intersect_func" : self.mapredIntersect(),
                    "toObj" : self.toObj(),
                } ); 

        # for each char1 in db which has one_element
  #   for each char2 in db which has max_elements
  #	create new char1_charMax and intersect char1.val charMax.val
  # repeat until max_elements == Maximum one element characteristics


    def mapfunc(self):

      # mongodb wants javascript for map reduce
    # checks: don't join me with myself; 
    ##	      if I am a joined ID, ignore me unless I am a max size concatenation;
    #	      if the ID you want to join me with, is already joined, ignore it;
    #	      if I already contain the ID you want to join me with, ignore it;
    #
    # BUGS: somehow the grouper creates DB_entries with the name in the _id
    # section, I guess its a mongodb internal thing. 
    #	I think it's the grouper, as the summarist is not writing to _id
    # ERROR: Cannot wirte property name to read-only object
    #	Where the fuck is that coming frome? 
        return """function map( ) {
            self = this;
            ids.forEach( function( x ) 
            {
                if( self.name == x ) return;
                if( self.name.split('_').indexOf(x) != -1 ) return;
                emit( [self.name, x].sort().join('_'), self.value );
            })
        }; """

    def reducefunc(self):
        return """function reduce( key, values ) {
            //print(key)
            //print(values)
            var test = eval( intersect_func )
            //print(test)
            ret = test.apply(null, values);
            //print( "ret: " +ret);
            //print( Object.prototype.toString.call(ret) )
            eval( toObj )
            ret = toObj(ret)
            //print( Object.prototype.toString.call(ret) )
            return ret;
      };
      """


    def mapredIntersect(self):
        return """intersect_func = function( a, b ) {
        return a.filter( function(x) { return b.indexOf(x) >= 0; });
          };"""

    def toObj(self):
        return """function toObj(arr) {
            var rv = {};
            for( var i = 0; i < arr.length; ++i )
                if( arr[i] !== undefined ) rv[i] = arr[i];
            return rv;
        }"""


#  def cleanup(self):
    # if group has not enough members 
    #	mark as uninteresting

    def run(self, mapred ):
        if mapred:
            self.grouping();
        else:
            self.combineIdents();



if __name__ == "__main__":
    grouper = Grouper()
    grouper.identDbSetup()
    print "identDBsetup done"
    grouper.grouping();
    print "grouping done"

#    grouper.combineIdents()
#    print "combineIdents done"


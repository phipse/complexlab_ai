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
        self.empty = int(0)
        self.content = int(0)
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
                value = ele['_id'];
                # if identifier already in the DB, update the value aka
                # characteristics list
                cursor = idDb.find( {'_id' : key })
                if cursor.count() > 0:
                    for oldEntry in cursor:
                        valueDict = oldEntry['value']
                        valueDict[str(len(valueDict))] = value;
                        idDb.update( {'_id' : key }, { "$set" : { "value" : \
                            valueDict } } )
                else:
                    idDb.insert( {'_id': key, 'value': { "0" : value} } )
        logging.debug("New database setup: idents")



    def combineIdents(self): 
        '''Combines two entries and intersects the characteristic lists'''

        logging.debug( "Grouping via combineIdents" )
        idDb = self.__db.idents
        combIdDb = self.__db.combIds
        if combIdDb.find().count() == 0: 
            for x in idDb.find():
                combIdDb.insert(x)

        for x in range(0,3):
            logging.debug("%s round-trip", x)
            for ele in list(idDb.find()):
                for snd in list(combIdDb.find()):
                    if ele == snd:
                        continue;
                    if not self.namePartial( ele['_id'], snd['_id'] ):
                        newKey = "_".join( sorted( set( \
                            sorted( (ele['_id']).split('_') ) + \
                            sorted( (snd['_id']).split('_') )  ) ) )
                        if combIdDb.find( {'_id' : newKey} ).count() == 0:
                            newValue = self.intersect( ele['value'], snd['value'] )
                            if len(newValue) != 0:
                                    toInsert = {'_id' : newKey, 'value' : \
                                        newValue }
                                    combIdDb.insert( toInsert  )
#                                    logging.debug( "Combined Ident inserted: %s", \
#                                            toInsert )
        logging.debug("Combine done: empty intersections: %i, other: %i", \
            self.empty, self.content)
                    

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
        res = list()
        for x in first:
            for y in second:
                if x == y:
                    res.append(x)
        sorted( res )
        if len(res) == 0:
            self.empty += 1
        else:
            self.content += 1
        return res



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
    def addFirstToSecond(self, first, second):
        for x in first.find():
            second.insert(x)

    def grouping2(self):
        logging.debug( "Grouping run two, directly on returend collection" );
        self.addFirstToSecond(self.__db.idents, self.__db.reduced);
        IDs = self.__db.reduced.distinct('_id')
        ret = self.__db.reduced.map_reduce( \
                self.mapfunc(), \
                self.reducefunc(), \
                "reduced2", \
                scope= { "ids": IDs, "intersect_func" : self.mapredIntersect()
                } ); 
        self.__db.reduced2.remove( {"value" : { } } ) 
        logging.debug("Mapreduce run 2 returned: %s", ret )



# mongo shit
    def grouping(self):
        ''' On basis of the db.idents collection map reduce is executed to generate
        all combinations '''
        # idDbSetup done; "_id", "name", "value"
        
        logging.debug( "Grouping via MapReduce" );
        IDs = self.__db.idents.distinct('_id')
        ret =  self.__db.idents.map_reduce( \
                self.mapfunc(), \
                self.reducefunc(), \
                "reduced", \
                scope= { "ids": IDs, "intersect_func" : self.mapredIntersect()
                } ); 
        self.__db.reduced.remove( {"value" : { } } ) 
        logging.debug("Mapreduce returned: %s", ret )

        # for each char1 in db which has one_element
  #   for each char2 in db which has max_elements
  #	create new char1_charMax and intersect char1.val charMax.val
  # repeat until max_elements == Maximum one element characteristics


    def mapfunc(self):

      # mongodb wants javascript for map reduce
    # checks: don't join me with myself; 
    #	      if I already contain the ID you want to join me with, ignore it;
    # not checked: If the reduced intersection is empty

        return """function map( ) {
            print( ids  + " " + ids.length)
            self = this;
            ids.forEach( function( x ) 
            {
                if( self._id == x ) return;
                if( self._id.split('_').indexOf(x) != -1 ) return;
                emit( [self._id, x].sort().join('_'), self.value );
            })
        }; """

    def reducefunc(self):
        return """function reduce( key, values ) {
            print(key)
           
            var test = eval( intersect_func )
            ret = test.apply(null, values);
            print( "ret: " +ret);
            print( "ret length: " + Object.keys(ret).length)
            return ret;
      };
      """


    def mapredIntersect(self):
        """Converts the passed dicts to local arrays and intersect them."""
        return """intersect_func = function( a, b ) {
        var arr1 = {}
        var counter = 0
        for( var key in a ) {
            for( var key2 in b)
            {
                if( a[key].toString() === b[key2].toString() )
                {
                   arr1[counter] = a[key]
                   counter = counter + 1
                }
            }
        }
        return arr1;

//        return arr1.filter( function(item) { 
//            if((arr2.toString().indexOf(item.toString()) != -1)) {
//                print( item )
//                print( arr2.toString().indexOf(item.toString()) )
//                return true;
//                }
//            else 
//                return false;
//            })
//            return (arr2.toString().indexOf(item.toString()) != -1) } )
          };"""


#  def cleanup(self):
    # if group has not enough members 
    #	mark as uninteresting

    def run(self, mapred ):
        if mapred:
            self.grouping();
            self.grouping2();
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


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
        if combIdDb.find().count() == 0: 
            for x in idDb.find():
                combIdDb.insert(x)

        for x in range(0,3):
            logging.debug("%s round-trip", x)
            for ele in list(idDb.find()):
                for snd in list(combIdDb.find()):
                    if ele == snd:
                        continue;
                    if not self.namePartial( ele['name'], snd['name'] ):
                        newKey = "_".join( sorted( set( \
                            sorted( (ele['name']).split('_') ) + \
                            sorted( (snd['name']).split('_') )  ) ) )
                        if combIdDb.find( {'name' : newKey} ).count() == 0:
                            newValue = self.intersect( ele['value'], snd['value'] )
                            if len(newValue) != 0:
                                    toInsert = {'name' : newKey, 'value' : newValue}
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
    def arrToObj(self, arr):
        ret = dict()
        for index,item in enumerate(arr):
            ret[str(index)]=item
        return ret;
            

    def joinIdentReduced(self):
        for x in self.__db.idents.find():
            x["_id"] = x["name"]
            del x["name"]
            x["value"] = self.arrToObj(x["value"])
            self.__db.reduced.insert(x)

    def grouping2(self):
        logging.debug( "Grouping run two, directly on returend collection" );
        self.joinIdentReduced();
        IDs = self.__db.reduced.distinct('name')
        ret = self.__db.reduced.map_reduce( \
                self.mapfunc(), \
                self.reducefunc(), \
                "reduced2", \
                scope= { "ids": IDs, "intersect_func" : self.mapredIntersect(),
                    "toObj" : self.toObj(),
                } ); 



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
                if( self.name == x ) return;
                if( self.name.split('_').indexOf(x) != -1 ) return;
                emit( [self.name, x].sort().join('_'), self.value );
            })
        }; """

    def reducefunc(self):
        return """function reduce( key, values ) {
            print(key)
            
            var test = eval( intersect_func )
            //print(test)
            ret = test.apply(null, values);
            print( "ret: " +ret);
            //print( Object.prototype.toString.call(ret) )
            eval( toObj )
            ret = toObj(ret)
            //print( Object.prototype.toString.call(ret) )
            return ret;
      };
      """


    def mapredIntersect(self):
        return """intersect_func = function( a, b ) {
        return a.filter( function(item) { return (b.toString().indexOf(item.toString()) != -1) } )
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


#!/bin/python

from pymongo import MongoClient

class Grouper:
  first = True
  db

  def init(self):
    connection = MongoClient()
    self.db = connection.complexlab_ai
    # open DB connection
    # test connection to DB
  
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
  # while there is data:
  # aquire dataset from the DB 
  # for data in dataset: extract the featureset
  # if featuresetgroup doesn't exist
  #   open new group
  # else:
  #   get group
  # add data to group

  def cleanup(self):
    # if group has not enough members 
    #	mark as uninteresting

  def run(self):
    if first: 
      init()
      first = False





if __name__ == "__main__":
  grouper = Grouper()
  grouper.run()
  

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
  # for each char1 in db which has one_element
  #   for each char2 in db which has max_elements
  #	create new char1_charMax and intersect char1.val charMax.val
  # repeat until max_elements == Maximum one element characteristics


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
  

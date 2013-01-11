import sys
import os

def createSymbolFile(inName):
  inf = file( inName, "r" )
  outname = inf.name + "_syms"
  if os.path.isfile(outname):
    return
  else:
    outf = file( outname, "a" )
  
  inf.readline() #ommit first description line
  for line in inf.readlines():
    outf.write( line.split("\t")[0] + "\n" )

  outf.flush()
  outf.close()
  inf.close()


if __name__ == "__main__":
  createSymbolFile( sys.argv[1] )


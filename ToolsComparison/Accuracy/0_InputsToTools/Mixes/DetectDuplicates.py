from sys import *

nameDict = {}

for line in open(argv[1]):
   name = line.strip().split("\t")[0]
   if name in nameDict:
      print line.strip()
      print nameDict[name].strip()
      print
   else:
      nameDict[name] = line

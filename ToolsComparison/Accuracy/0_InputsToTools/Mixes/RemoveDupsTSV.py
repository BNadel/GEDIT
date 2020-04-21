from sys import *

nameDict = {}
first = True
for line in open(argv[1]):
   name = line.strip().split("\t")[0]
   if first:
     firstLength = len(line.strip().split("\t"))
     first = False
   else:
     length = len(line.strip().split("\t"))
     if length != firstLength:
        continue
   if name not in nameDict and len(name) > 0 and name != "NA":
      nameDict[name] = 0
      print line.strip()


import sys

FileName = sys.argv[1]

partsList = []
for line in open(FileName,"r"):
   partsList.append(line.strip().split("\t"))

CellTypes = partsList[0][1:]

print "Sample" + "\t" + "Cell Type" + "\t" + "Value"
for parts in partsList[1:]:
    Sample = parts[0]
    for i in range(len(parts[1:])): 
       print Sample + "\t" + CellTypes[i] + "\t" + parts[i+1]

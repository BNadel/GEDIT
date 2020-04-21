from sys import *
EnsToGS = {}

for line in open(argv[1], "r"):
  parts = line.strip().split()
  EnsToGS[parts[0]] = parts[1]

EnsToLength = {}
first = True
for line in open(argv[2], "r"):
  if first:
     print line.strip()
     first = False
  parts = line.strip().split("\t")
  EnsToLength[parts[0]] = parts[1]
  if parts[0] in EnsToGS:
    print parts[0] + "\t" + EnsToGS[parts[0]] +"\t" + "\t".join(parts[1:])  

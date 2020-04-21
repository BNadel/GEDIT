lineMat = []
for line in open("ByTissueName.tsv", "r"):
   lineMat.append(line.strip().split("\t"))


header = lineMat[0]
for parts in lineMat[1:]:
  for i in range(1,len(parts)):
    print parts[0] + "\t" +  header[i] + "\t" + parts[i]

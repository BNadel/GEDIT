def main():
 ConvDict = {}
 inMat = []
 for line in open("GTEXSampleNames.tsv","r"):
   inMat.append(line)

 for line in inMat[1:]:
   parts = line.strip().split("\t")
   Dotted = ".".join(parts[0].split("-"))
   ConvDict[Dotted] = parts[1]
  
 inMat2 = []
 for line in open("BlueCodePredictionsCollapsed.csv","r"):
   inMat2.append(line)
 print "\t".join(inMat2[0].split(","))
 for line in inMat2[1:]:
   parts = line.strip().split(",")
   try:
     new0 = ConvDict[parts[0]]
     print "\t".join([new0] + parts[1:])
   except:
     continue

main()

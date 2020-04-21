import sys
def main():
 ConvDict = {}
 TissuesDict = {} #keys are tissue, values are a list of vectors
 inMat = []
 for line in open("GTEXSampleNames.tsv","r"):
   inMat.append(line)

 for line in inMat[1:]:
   parts = line.strip().split("\t")
   Dotted = ".".join(parts[0].split("-"))
   ConvDict[Dotted] = parts[1]
  
 inMat2 = []
 for line in open(sys.argv[1],"r"):
   inMat2.append(line)
 print "Tissue" + "\t" + "\t".join(inMat2[0].split(","))
 for line in inMat2[1:]:
   parts = line.strip().split(",")
   try:
     new0 = ConvDict[parts[0]]
     if new0 not in TissuesDict:
      TissuesDict[new0] = []
     TissuesDict[new0].append(parts[1:])
   except:
     continue

 for tissue in TissuesDict: 
   Averages = CalcAverages(TissuesDict[tissue])
   print tissue + "\t" + "\t".join(Averages)

def CalcAverages(ManyPreds):
   outVec = [0]*len(ManyPreds[0])
   for FewPreds in ManyPreds:
     for i in range(len(FewPreds)):
       outVec[i] += float(FewPreds[i])
   for i in range(len(outVec)):
     outVec[i] = str(outVec[i]/float(len(ManyPreds)))

   return outVec

main()

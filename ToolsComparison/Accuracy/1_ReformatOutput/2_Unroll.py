import sys

FileList = sys.argv[1]
TrueProps = sys.argv[2]

flist = []
for line in open(FileList,"r"):
  flist.append(line.strip())

partsList = []
for line in open(TrueProps,"r"):
   partsList.append(line.strip().split("\t"))

CellTypes = partsList[0]
AnswersD = {}   #dictionary that has true proportion for each key of SAMPLE_CELLTYPE
for parts in partsList[1:]:
   Sample = parts[0]
   for i in range(1,len(parts)):
     CellType = CellTypes[i]
     Answer = str(round(float(parts[i]),3))
     AnswersD[Sample + "_" + CellType] = Answer

print "\t".join(["Tool-Reference","CellType","Sample","Prediction", "Answer", "Error", "SqError"])
for fname in flist:
   ToolName = fname.split(".")[-2].split("/")[-1].split("_")[0]
   RefName = fname.split(".")[-2].split("_")[-1]

   fstream = open(fname,"r")
   predictionsMatrix = []
   for line in fstream:
     predictionsMatrix.append(line.strip().split("\t"))
  
   for predVector in predictionsMatrix[1:]:
     Sample = predVector[0]
     for i in range(1,len(predVector)):
        CellType = CellTypes[i]
        prediction = float(predVector[i])
        trueProp = float(AnswersD[Sample + "_" + CellType])
        error = abs(trueProp - prediction)
        sqError = error*error
        outList = [ToolName + "-" +  RefName,CellType,Sample,prediction, trueProp, error, sqError]
        print "\t".join([str(m) for m in outList])

from sys import *
from math import *
"""
TODO:Crashes becaure readmatrix file expectes top left corner to be filled


returns table, one row per prediction, columns are metadata about that prediciton
                                       predicted value, true value, cell type

Alpha4,5,6,10 are assumed to be in the same directory

argv[1] is text file containing list of prediction files to be summarized
                                        these are matrices of .tsv form
"""
def main():
 outList = []
  
 for line in open(argv[1],"r"):
  fName = line.strip()
  Settings = ParseSettings(fName)
  AnsKey = Settings[-1]
  out = SummarizePredictions(fName,AnsKey)
  temp = []
  for el in out:
    print el 
 #temp.append("\t".join([dimValue,str(el)]))
    
 #print "\n".join(outList)

def SummarizePredictions(F1,F2):
    outList = []
    M1 = readMatrix_keepFirstLine(F1)
    M1Names = M1[0]
    M1 = M1[1:]
    M2 = readMatrix_keepFirstLine(F2)
    M2Names = M2[0]
    M2 = M2[1:]
    for i in range(len(M2)):
      for j in range(len(M2[i])):
        Prediction = float(M1[i][j])
        Actual = float(M2[i][j])
        Error = Prediction - Actual
        CellType = M1Names[j]
        curMeta = [Prediction, Actual, Error, CellType, F1]
        outList.append("\t".join([str(m) for m in curMeta]))
  
    return outList

def ParseSettings(fName):
  """
  given a file name, returns list of parameter settings, and AK file
  """
  parts = fName.split("_")
  if "Alpha4" in fName:
    AnsKey = "Alpha4.tsv"
  elif "Alpha5" in fName:
    AnsKey = "Alpha5.tsv"
  elif "Alpha6" in fName:
    AnsKey = "Alpha6.tsv"
  elif "Alpha10" in fName:
    AnsKey = "Alpha10.tsv"
  outList = parts[3:6] + [parts[6].split("P")[0]] + [AnsKey] #MinSigs, AvgSigs, Method, RowScaling
  return outList


def readMatrix_keepFirstLine(File):
  Matrix = []
  for line in open(File, "r"):
    toAdd = line.strip().split("\t")
    if len(toAdd) == 1:
      toAdd = line.strip().split(",")
    if len(toAdd) == 1:
      toAdd = line.strip().split(" ")
    Matrix.append(toAdd)

  trimmedMat = []
  if len(Matrix[0]) == len(Matrix[1:]):
    #i.e. if the topleft corner is filled
    trimmedMat.append(Matrix[0][1:])
  else:
    trimmedMat.append(Matrix[0])

  for parts in Matrix[1:]:
    trimmedMat.append(parts[1:])
  return trimmedMat


def OthersDefault(Settings, Defaults, dimension):
  """
  if parameters other than dimension (an integer) are defaults, return True
  """
  TakeIt = True
  for i in range(1,4):
     if i == dimension:
       continue
     if Settings[i] != Defaults[i]:
       TakeIt = False

  if Settings[1] != Settings[0] and dimension != 0:
    TakeIt = False

  return TakeIt  
main()

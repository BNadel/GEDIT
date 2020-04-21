from sys import *
from math import *
"""
argv[1] is text file containing list of prediction files
argv[2] is the dimension to be visualized (0,1,2,3)
"""
def main():
 outList = []
 Defaults = ["50","50","Entropy","0.0"]
 Dimension = int(argv[2])  #parameter value to view, with others as defaults
  
 for line in open(argv[1],"r"):
  fName = line.strip()
  Settings = ParseSettings(fName)
  AnsKey = Settings[-1]
  Settings = Settings[0:-1]
  TakeIt = OthersDefault(Settings, Defaults, Dimension)
  shortFName = fName[10:35]
  if TakeIt:
    dimValue = Settings[Dimension]
    curErrorList = CalcAllErrors(fName,AnsKey)
    temp = []
    for el in curErrorList:
       temp.append("\t".join([dimValue,str(el),shortFName]))
    outList = outList + temp
    
 print "\n".join(outList)

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

def ParseSettings(fName):
  """
  given a file name, returns list of parameter settings, and 
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


def readMatrix(File):
  Matrix = []
  first = True
  for line in open(File, "r"):
    if first:
      first = False
      continue
    toAdd = line.strip().split("\t")[1:]
    if len(toAdd) == 1:
      toAdd = line.strip().split(",")[1:]
    if len(toAdd) == 1:
      toAdd = line.strip().split(" ")[1:]
    Matrix.append(toAdd)
  return Matrix

def CalcAllErrors(F1,F2):
   outList = []
   try:
    M1 = readMatrix(F1)
    M2 = readMatrix(F2)
    for i in range(len(M2)):
      TotalError = 0
      TotalSqError = 0
      for j in range(len(M2[i])):
        TotalError += abs(float(M1[i][j]) - float(M2[i][j]))
        TotalSqError += (float(M1[i][j]) - float(M2[i][j]))**2
      AvgError = TotalError/len(M2[0])
      outList.append(round(AvgError,5))
  
    return outList

   except:
    print F1, "\t", "at least one crash"
    return
main()

import MatrixTools
"""
Parses the input submitted by the user. Checks that each input is valid.
If all inputs valid, returns them as a list. If an input is invalid,
returns False, ErrorMessage
"""

def argsToDict(ArgList):
  argDict = {}
  for i in range(len(ArgList)):
     if ArgList[i][0] == "-":
       try:
         argDict[ArgList[i][1:]] = ArgList[i+1]
       except:
         argDict[ArgList[i][1:]] = None
  return argDict

def checkInputs(InputString):
  argDict = argsToDict(InputString)
 
  if "mix" not in argDict:
    return False, "Mixture matrix not specified. Please indicate\
               a mixture file using the argument -mix myfile.tsv"

  MixFName = argDict["mix"]
  Mix = MatrixTools.readMatrix(MixFName)
  mixCheck = checkMatrix(Mix)
  if mixCheck != True:
    return False, "An error was detected with your\
     submitted mixture file:\n" + mixCheck

  if "ref" not in argDict:
    return False, "reference matrix not specified. Please indicate\
               a reference file using the argument -ref myfile.tsv"
  RefFName = argDict["ref"]
  Ref = MatrixTools.readMatrix(RefFName)
  refCheck = checkMatrix(Ref)
  if refCheck != True:
    return False,"An error was detected with your\
                 submitted reference file:\n" + refCheck
  
  if "outFile" in argDict:
     outFile = argDict["outFile"]
  elif "out" in argDict:
     outFile= argDict["out"]
  else:
     outFile = "None"

  if "NumSigs" in argDict:
    totalSigs = argDict["NumSigs"]
    try:
      totalSigs  = int(totalSigs)
      if totalSigs < 1 or totalSigs > 10000:
        return False, "invalid numSigs:  " + totalSigs
    except:
      return False, "invalid numSigs:  " + totalSigs
  else:
    totalSigs = 50

  if "MinSigs" in argDict:
    MinSigsPerCT = argDict["MinSigs"]
    try:
      MinSigsPerCT = int(MinSigsPerCT)
      if MinSigsPerCT < 1 or MinSigsPerCT > totalSigs:
        return False, "invalid MinSigsPerCT" + MinSigsPerCT
    except:
      return False, "invalid MinSigsPerCT" + MinSigsPerCT
  else:
    MinSigsPerCT = totalSigs

  if "SigMethod" in argDict:
    SigMethodList = argDict["SigMethod"] 
    for SigMethod in SigMethodList.split(","):
      if SigMethod not in ["Intensity","Entropy",\
      "Zscore","MeanRat","MeanDiff","fsRat","fsDiff","IntEnt"]:
        return False, "invalid sigMethod" + SigMethodList
  else:
    SigMethodList = "Entropy"

  if "RowScaling" in argDict:
    try:
      RowScaling = float(argDict["RowScaling"])
      if float(RowScaling) > 1.0 or float(RowScaling) < 0.0:
        print("invalid RowScaling", RowScaling)
        return False
    except:
      print("invalid RowScaling", argDict["RowScaling"])
      return False
  else:
    RowScaling = 0.0

  if "saveFiles" in argDict:
      argDict["SaveFiles"] = argDict["saveFiles"]
  if "saveFile" in argDict:
      argDict["SaveFiles"] = argDict["saveFiles"]
  if "SaveFile" in argDict:
      argDict["SaveFiles"] = argDict["saveFiles"]
  if "SaveFiles" in argDict:
      if argDict["SaveFiles"].lower() in ["yes","true","all"]:
        SaveFiles = "All"
      elif argDict["SaveFiles"].lower() in ["none","no","false"]:
        SaveFiles = "None"
      else:
        SaveFiles = "Some"
  else:
      SaveFiles = "Some"
     
  return [Mix, Ref, totalSigs, MinSigsPerCT, SigMethodList, RowScaling, MixFName, RefFName, outFile,SaveFiles]


def checkMatrix(matrix):
  """
  returns True if matrix is ok, otherwise returns text describing error
  """

  nameLength = len(matrix[0])

  for row in matrix[1:]:
     if len(row) != nameLength:
       print(row)
       return "this row is not of the same length as the first: \n" + "\t".join([str(m) for m in row[:10]])

     if len(row) == 1:
       return "The system is detecting only 1 column in your\
        matrix. Please check that the fields in your file \
        are separated by commas or tab charectors"
     for el in row[1:]:
       try:
         float(el)
       except:
         return "non-numeric value in the matrix: " + str(el)
  
  return True

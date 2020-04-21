from sys import *
"""
TODO: 
    verify that all cell type labels are properly interpreted
    Manually check addition is done correctly
"""
"""
Purpose of this script:
Depending on the tool, reference, and mixture, the columns of the
outputs may need to me reordered or combined to match the answerkey
"""

def ConvertNames(namesList, Set):
    newNames = []
    for oldName in namesList:
       if Set == "CellMixtures":
         newNames.append(Convert1NameCellMix(oldName))
       elif Set == "CellMix":
         newNames.append(Convert1NameCellMix(oldName))
       elif Set == "Hoek":
         newNames.append(Convert1NameHoek(oldName))
       elif Set == "Ascites":
         newNames.append(Convert1NameAscites(oldName))
       elif Set == "BothTCellMix":
         newNames.append(Convert1NameCellMixBothT(oldName))
       else:
         print "not recognized", Set
    #print "\t".join(namesList)
    #print "\t".join(newNames)
    return newNames



def Convert1NameAscites(Name):
  name = Name.lower()
  if "mast" in name:
     return "Other"

  if "cd4" in name or "cd8" in name\
          or "t_cell" in name\
          or "t cell" in name:
     return "T Cells"

  if "mono" in name or "macro" in name or name in ["M0","M1","M2","M3"]:
      return "Monocytes"

  if "neut" in name:
      return "Neutrophils"

  if "b cell" in name\
      or "b.cell" in name\
      or "b_cell" in name:
      return "B Cells"

  if "dendritic" in name:
      return "Other"

  if "nk" in name\
      or ("natural" in name and "killer" in name):
      return "NK"

  if name in ["p-value", "correlation", "rmse","absolute score (sig.score)"]:
     return "Excluded"
  return "Other"

def Convert1NameCellMix(Name):
  name = Name.lower()
  if "mast" in name:
     return "Other"

  if "cd4" in name or "cd8" in name\
     or "t cell" in name\
     or "t_cell" in name\
     or "t.cell" in name:
     return "T Cells"

  if "mono" in name:
      return "Monocytes"

  if "neut" in name:
      return "Neutrophils"

  if "b cell" in name\
      or "b.cell" in name\
      or "b_cell" in name:
      return "B Cells"

  if "dendritic" in name:
      return "Other"

  if "nk" in name\
      or ("natural" in name and "killer" in name):
      return "NK"

  if name in ["p-value", "correlation", "rmse","absolute score (sig.score)"]:
     return "Excluded"
  return "Other"

def Convert1NameCellMixBothT(Name):
  name = Name.lower()
  if "mast" in name:
     return "Other"

  if "cd4" in name:
     return "CD4 T Cells"

  if "cd8" in name:
     return "CD8 T Cells"

  if "mono" in name:
      return "Monocytes"

  if "neut" in name:
      return "Neutrophils"

  if "b cell" in name\
      or "b.cell" in name\
      or "b_cell" in name:
      return "B Cells"

  if "dendritic" in name:
      return "Other"

  if "nk" in name\
      or ("natural" in name and "killer" in name):
      return "NK"

  if name in ["p-value", "correlation", "rmse","absolute score (sig.score)"]:
     return "Excluded"
  return "Other"

def Convert1NameHoek(Name):
  name = Name.lower()
  if "mast" in name:
     return "Other"
  if "t.cells" in name\
     or "t cell" in name\
     or "t_cell" in name\
     or "t.cell" in name:
     return "T Cells"

  if "mono" in name:
      return "Monocytes"

  if "b cell" in name\
      or "b.cell" in name\
      or "b_cell" in name:
      return "B Cells"

  if "dendritic" in name:
      return "Other"

  if "nk" in name\
      or ("natural" in name and "killer" in name):
      return "NK"

  if name in ["p-value", "correlation", "rmse","absolute score (sig.score)"]:
     return "Excluded"
  return "Other"

def combineColumns(predMat, colsToCombine):
    ConvertedMat = []
    for lineParts in predMat:
      ConvertedLine = [lineParts[0]]
      for group in colsToCombine:
        groupSum = 0
        for col in group:
          try:
            groupSum += float(lineParts[col+1])
          except:
            continue
        ConvertedLine.append(str(round(groupSum,5)))
      ConvertedMat.append(ConvertedLine)
    return ConvertedMat

def ReformatPredictions(predictionsFile, AnsCTs):
    """
    Identifies columns in predictions file that correspond to the columns of the answer file
    in the case of multiples pred CTS that map to the same AnsCT, takes the sum
    """
    predMat = []
    Set = argv[3]

    for line in open(predictionsFile,"r"):
      splitLine = line.strip().split("\t")
      if len(splitLine) == 1:
         splitLine = line.strip().split(",")
      predMat.append(splitLine)


    if len(predMat[0]) == len(predMat[1]):
       #i.e. something like "gene" fills top left corner
       convertedNames = ConvertNames(predMat[0][1:],Set)
       t = 1
    else:
       convertedNames = ConvertNames(predMat[0],Set)
       t = 0


    #initialize list of columns to combine
    colsToCombine = []
    for i in range(len(AnsCTs)):
        colsToCombine.append([])

    for i in range(len(AnsCTs)):
      AnsCT = AnsCTs[i]
      for j in range(len(convertedNames)):
        predCT = convertedNames[j]
        if predCT == AnsCT:
          colsToCombine[i].append(j)
    Reformatted = combineColumns(predMat[1:], colsToCombine)
    return Reformatted       

    
def main():
   AnsFile = open(argv[2],"r")
   for line in AnsFile:
     AnsCTs = line.strip().split("\t")[1:]
     break
   NewPreds = ReformatPredictions(argv[1],AnsCTs)# + ["Other"])
   print "\t" + "\t".join(AnsCTs)# + ["Other"])
   for line in NewPreds:
      pass
      print "\t".join(line)
main()

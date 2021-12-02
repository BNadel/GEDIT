import sys
import statistics
from math import log

def returnSigMatrix(inMat,minPerCT,TotalSigs,strModes):
  """
  Identify Signature Genes and return matrix 
  contaning only those genes (others discarded)
  """
  validModes = ["Intensity","Entropy","Zscore",\
               "MeanRat","MeanDiff","fsRat","fsDiff"]


  trimmed = trimIncomplete(inMat[1:], .5)

  unZerod = UnZeroMatrix([inMat[0]] + trimmed)
 
  modeList = strModes.split(",")
  if len(modeList) == 0:
    return "No signature gene selection mode chosen"
  for mode in modeList:
    if mode not in validModes:
      return "Invalid sigature gene selection mode chosen: " + str(mode)\
          + "\n" + "valid modes:", "\t".join(validModes)

  scoresList = []
  for mode in modeList:
    scoresList.append(generateScores(unZerod, mode))

  if len(modeList) > 1:
    scoresByCT = rankCombineGenerateScores(scoresList)

  else:
    scoresByCT = scoresList[0]

  sigGenes = identifySigGenes(scoresByCT, minPerCT, TotalSigs)

  sigMat = [inMat[0]]
  
  for line in inMat:
     if line[0].upper() in sigGenes:
       sigMat = sigMat + [line]

  return sigMat

def UnZeroMatrix(matrix):
  """
  replaces all instances of 0.0000 in the 
  matrix with the lowest observed non-zero value
  assumes first row and first column of matrix are
  descriptors
  """
  minNonZero = min([float(m) for m in matrix[1][1:]])
  for line in matrix[2:]:
    for el in line[1:]:
      if float(el) != 0.000 and float(el) < minNonZero:
        minNonZero = float(el)

  newMat = [matrix[0]]
  for line in matrix[1:]:
    curVec = [line[0]]
    for el in line[1:]:
      if float(el) == 0.000:
        curVec.append(minNonZero)
      else:
        curVec.append(float(el))
    newMat.append(curVec)
  return newMat
     
def rankCombineGenerateScores(ScoresList):
  """
  orders genes based on each scoring method in modesList,
  and returns their scores as sum of ranks when ordered by these methods
  """

  MaxCTDict = {}
  for ct in ScoresList[0]:
    for pair in ScoresList[0][ct]:
      MaxCTDict[pair[1]] = ct
  
  totalRanks = {} 
  for curScores in ScoresList:
    listScores = []
    for ct in curScores:
      for pair in curScores[ct]:
        score = pair[0]
        geneName = pair[1] 
        listScores.append([score,geneName])
    sortedScores = sorted(listScores)[::-1]

    for i in range(len(sortedScores)):
      score = sortedScores[i][0]
      geneName = sortedScores[i][1]
      if geneName not in totalRanks:
        totalRanks[geneName] = 0
      totalRanks[geneName] += i
  
  scoresByCT = {}
  for gene in totalRanks:
    ct = MaxCTDict[gene]
    if ct not in scoresByCT:
      scoresByCT[ct] = []
    totalRank = totalRanks[gene]
    scoresByCT[ct].append((-1*totalRank, gene))
    # we negate here so that low rank is highest score
  return scoresByCT

def generateScores(ExpressionMatrix, mode):
  """
  input-- matrix of expression values:
     first column gene symbols, first row cell type names
  output-- A dictionary formated as:
     keys = cell types, values = (score,gene) tuple
  """
  CellTypeD = {}
  for line in ExpressionMatrix[1:]:
    geneName = line[0]
    floatExps = [float(m) for m in line[1:]]    
    bigVal = max(floatExps)
    bigIndex = floatExps.index(bigVal)
    nameBig = ExpressionMatrix[0][bigIndex+1]
    #nameBig is the Cell Type of maximum expression

    if nameBig not in CellTypeD:
      CellTypeD[nameBig] = []

    score = genScore(mode, floatExps)
    CellTypeD[nameBig].append((score,geneName))
  
  return CellTypeD

def identifySigGenes(scoresByCT, minPerCT, TotalSigs):
  """
  scoresByCT is a dictionary containing a list of possible signatures for each cell type
  This function returns a list of N=TotalSigs signatures
      the minPerCT best for each cell type
      and TotalSigs total
  """
  localBest = []
  for CT in scoresByCT:
    curSigs = bestNScores(scoresByCT[CT],minPerCT)
    localBest = localBest + curSigs

  bigList = [] #combine sigs categorized by CT into one list of all sigs
  for pairsList in scoresByCT.values():
     bigList = bigList + pairsList
    
  for gene in localBest:
    #remove from the combined list genes already selected as sigs
    bigList.remove(gene)
  
  #select the best sigs out of the remaining
  numLeftToGet = TotalSigs-len(localBest)
  if numLeftToGet > 0:
    globalBest = bestNScores(bigList, TotalSigs - len(localBest))
    AllPairs = globalBest + localBest
  else:
    AllPairs = localBest
  AllSigs = []
  for pair in AllPairs:
    AllSigs.append(pair[1])  

  return AllSigs


def bestNScores(scoresList,N):

  sortedList = sorted(scoresList)
  if len(sortedList) < N:
    return sortedList
  return sortedList[-N:]

def genScore(mode, floatExps):
    if mode == "Intensity":
      Intensity = sum(floatExps)
      Score = Intensity

    elif mode == "NegEntropy" or mode == "Entropy":
      NegEntropy = scoreGeneEntropy(floatExps)
      Score = NegEntropy

    elif mode == "Zscore":
      Zscore = scoreGeneMeanComparison(floatExps, "Zscore")
      Score = Zscore

    elif mode == "MeanDiff":
      MeanDiff = scoreGeneMeanComparison(floatExps, "MeanDiff")
      Score = MeanDiff

    elif mode == "MeanRat":
      MeanRat = scoreGeneMeanComparison(floatExps, "MeanRat")
      Score = MeanRat

    elif mode == "fsRat":
      fsRat = scoreGene12(floatExps, "ratio") 
      Score = fsRat

    elif mode == "fsDiff":
      fsDiff = scoreGene12(floatExps, "difference") 
      Score = fsDiff

    else:
      print "invalid scoring method chosen", str(mode)
      return

    return Score

def remove0s(matrix):
     newMat = []
     for line in matrix:
        total = sum(line)
        if total > 0.0:
           newMat.append(line)

     return newMat

def assignAllSigGenes(refMat, TissueNames, mode, numSigs):

  refDict = {}
  for line in refMat:
     refDict[line[0]] = line

  numColumns = len(refDict[refDict.keys()[5]])-1
  if len(TissueNames) == numColumns + 1:
    TissueNames = TissueNames[1:]
  
  TissueDict = {}    #signature genes for each tissue
  for Tissue in TissueNames:
     TissueDict[Tissue] = []
  for geneName in refMat:
    ExpVals = refDict[geneName][1:]
    score, NameBig = scoreGeneModal(ExpVals, TissueNames, mode)
    TissueDict[NameBig].append((score,geneName))

  outMat = []
  for Tissue in TissueDict:
    entry = sorted(TissueDict[Tissue])
    for pair in entry[-1 *numSigs:]:
      geneToPrint = refDict[pair[1]]
      outMat.append(geneToPrint)
  return outMat

"""
Scoring Methods:
"""

def scoreGeneEntropy(StrExpVals):
  ExpVals = [float(i) for i in StrExpVals]
  RatiodVals = []
  #turn expression vals into probabilities that sum to 1
  for val in ExpVals:
    if val == 0:
      continue
    RatiodVals.append(float(val)/sum(ExpVals))
   
  entropy = -1* sum([log(i)*i for i in RatiodVals])
  return -1 * entropy

def scoreGene12(StrExpVals, mode):
  ExpVals = [float(i) for i in StrExpVals]
  biggest = max(ExpVals)
  ExpVals.remove(biggest)
  sndBiggest = max(ExpVals)
  if mode == "ratio":
     return biggest/max(sndBiggest,.00000001)
  elif mode == "diff" or mode == "difference":
     return biggest - sndBiggest

def scoreGeneMeanComparison(ExpressionVals, mode):
  if mode not in ["Zscore","MeanRat", "MeanDiff"]:
    print "improper usage, scoreGeneZScore"
    print mode
    return
  
  ExpressionVals = [float(i) for i in ExpressionVals]
  maxExp = max(ExpressionVals)
  ExpressionVals.remove(max(ExpressionVals))
  mean = sum(ExpressionVals)/float(len(ExpressionVals))
  
  if mode == "Zscore":
    spread = statistics.stdev(ExpressionVals)
    score = (maxExp-mean)/max(spread,.0000001)

  elif mode == "MeanRat":
    score = maxExp/max(mean, .000001)

  elif mode == "MeanDiff":
    score = (maxExp-mean)
  
  return score

"""
End Scoring Methods
"""

def trimIncomplete(Matrix, percent):
  """
  removes each gene with percent or more values of 0.0
  e.g. if percent = .4 and there are 10 observations for each gene, 
  all genes with 4 or more 0.0s will be excluded
  There must be at least 1 nonzero value
  
  """
  outMat = []
  for line in Matrix:
    N = len(line[1:])
    maxZeros = min((percent * N), N-1)

    numZeros = 0
    for el in line[1:]:
       if float(el) == 0:
          numZeros += 1
    if numZeros <= maxZeros:
      outMat.append(line)
  return outMat 
  

def trimLowIntensity(Matrix,ratio):
   """
   trim the bottom percentile of genes, as ranked by intensity
   if total intensity is 0.0, that gene is automatically excluded
   """
   Intensities = []
   for line in Matrix:
     intensity = 0
     for el in line[1:]:
       intensity += float(el)
     if intensity > 0.0:
       Intensities.append(intensity)
 
   cutoff = Intensities[int(ratio*len(Intensities))]

   outMat = []
   for line in Matrix:
     intensity = 0
     for el in line[1:]:
       intensity += float(el)
     if intensity > cutoff:
       outMat.append(line)
   return outMat

def readInMatrixToDict(fname):
  """
  splits all lines around tabs (or commas if no tabs
  present, then returns: 
  B) dictionary of all lines other than the first. keys are first element (i.e. gene name)
  A) the first line
  """
  Matrix = {}
  first = True
  for line in open(fname, "r"):
    parts = line.strip().split("\t")
    if len(parts) == 1:
      parts = line.strip().split(",")
    if first:
      first = False
      FirstLine = parts
      continue
    Matrix[parts[0]] = parts
    
  return Matrix, FirstLine

 
def median(lst):
   lst = [float(i) for i in lst]
   lst = sorted(lst)
   x = len(lst)
   if x == 0:
      print "error, 0"
      return
   if x%2 == 0:
     return (float(lst[x/2-1]) + float(lst[x/2]))/2
   else:
     return lst[x/2]


#!/usr/bin/python
import sys
import getSigGenesModal
import MatrixTools
import HandleInput
import os
import random
import numpy as np

def main():
  """
  usage default:
  python ThisScript.py -mix SamplesMat.tsv -ref RefMat.tsv

  user selected parameters:
  python ThisScript.py -mix SamplesMat.tsv -ref RefMat.tsv -numSigs SigsPerCT -method SigMethod -RS rowscaling
  """
  #where to write results 
  curDir = "/".join(os.path.realpath(__file__).split("/")[0:-1]) + "/"
  scratchSpace = curDir + "scratch/"

  myArgs = HandleInput.checkInputs(sys.argv[1:])
  if myArgs[0] == False:
    print myArgs[1:]
    return

  rawMix = myArgs[0]
  rawRef = myArgs[1]
  SigsPerCT = myArgs[2]
  #minSigs = myArgs[3]
  SigMethod = myArgs[4]
  RowScaling = myArgs[5]
  MixFName = myArgs[6].split("/")[-1]
  RefFName = myArgs[7].split("/")[-1]
  outFile = myArgs[8]

  numCTs = len(rawRef[0])-1
  TotalSigs = int(SigsPerCT*numCTs)
 
  stringParams = [str(m) for m in \
          [MixFName,RefFName,SigsPerCT,SigMethod,RowScaling]]
  
  scratchSpace = scratchSpace + "_".join(stringParams) + "_"

  SampleNames = rawMix[0]
  CTNames = rawRef[0]

  betRef = MatrixTools.remove0s(rawRef)
  
  normMix, normRef = MatrixTools.qNormMatrices(rawMix,betRef)
  sharedMix, sharedRef = MatrixTools.getSharedRows(normMix,betRef)

  if len(sharedMix) < 1 or len(sharedRef) < 1:
      print "error: no gene names match between reference and mixture"
      return
  if len(sharedMix) < numCTs or len(sharedRef) < numCTs:
      print "warning: only ", len(sharedMix) , " gene names match between reference and mixture"

  #write normalized matrices
  MatrixTools.writeMatrix([CTNames] + normRef, scratchSpace + "NormRef.tsv") 
  MatrixTools.writeMatrix([SampleNames] + normMix, scratchSpace + "NormMix.tsv")

  SigRef = getSigGenesModal.returnSigMatrix([CTNames] + sharedRef, \
  SigsPerCT, TotalSigs, SigMethod)
  
  SigMix, SigRef = MatrixTools.getSharedRows(sharedMix, SigRef)

  """
  write matrices with only sig genes. files are not used by this program,
  but potentially informative to the user
  """
  
  MatrixTools.writeMatrix([CTNames] + SigRef, scratchSpace + "SigRef.tsv") 
  ScaledRef, ScaledMix = MatrixTools.RescaleRows(SigRef[1:], SigMix[1:], RowScaling)
 
  ScaledRef = [CTNames] + ScaledRef
  ScaledMix = [SampleNames] + ScaledMix 

  refFile = scratchSpace + "ScaledRef.tsv"
  mixFile = scratchSpace + "ScaledMix.tsv"

  MatrixTools.writeMatrix(ScaledRef, refFile)
  MatrixTools.writeMatrix(ScaledMix, mixFile)
   
  strDescr = "_".join(stringParams)
  Rscript = "scripts/GLM_Decon.R"
  if outFile == None:
    outFile =  "predictions/" + "_".join(stringParams) + "Predictions.tsv"
  print "Rscript", Rscript, mixFile, refFile, outFile
  #predictions = Regression(scratchSpace, CTNames, SampleNames,refFile, mixFile,strDescr)
  #if predictions == False:
  #   return

  #for line in predictions:
  #  print "\t".join([str(el) for el in line])
  return

def readInPredictions(fname):
  PredictionStream = open(fname,"r")
  predictions = []
  first = True
  for line in PredictionStream:
     parts = line.strip().split(",")
     if len(parts) < 2: #i.e. its not csv, actually tsv
       parts = line.strip().split()
     if first:
       first = False
     else:
       parts = parts[1:]
     predictions.append(parts)
  return predictions

def Regression(scratchSpace, TissueNames, SampleNames, refFile, mixFile, strDescr):

  outFile = scratchSpace + "Out" 
  graphics = "NO"
  Rscript = "GLM_Decon.R"
  
  FNULL = open(os.devnull, "w")
  returnCode = subprocess.call(["Rscript", Rscript, mixFile, \
        refFile,outFile,strDescr],stdout=FNULL, stderr=FNULL)
  FNULL.close() 
  if not returnCode == 0:
     print "failed on first Deconvolution; exit code != 0" 
     print Rscript, mixFile, refFile, outFile
     return False

  predictions = MatrixTools.readMatrix(outFile + "_Predictions.tsv")
  return predictions

main()

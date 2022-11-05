#!/usr/bin/python
import sys
sys.path.insert(0,"scripts/")
#from scripts 
import getSigGenesModal
#from scripts 
import MatrixTools
#from scripts 
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

  myArgs = HandleInput.checkInputs(sys.argv[1:])
  if myArgs[0] == False:
    print myArgs[1:]
    return

  rawMix = myArgs[0]
  rawRef = myArgs[1]
  SigsPerCT = myArgs[2]
  #minSigs = myArgs[3]  not currently used
  SigMethod = myArgs[4]
  RowScaling = myArgs[5]
  MixFName = myArgs[6].split("/")[-1]
  RefFName = myArgs[7].split("/")[-1]
  outFile = myArgs[8]
  SaveFiles = myArgs[9]

  numCTs = len(rawRef[0])-1
  TotalSigs = int(SigsPerCT*numCTs)
 
  stringParams = [str(m) for m in \
          [MixFName,RefFName,SigsPerCT,SigMethod,RowScaling]]
  

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


  SigRef = getSigGenesModal.returnSigMatrix([CTNames] + sharedRef, \
  SigsPerCT, TotalSigs, SigMethod)
  
  SigMix, SigRef = MatrixTools.getSharedRows(sharedMix, SigRef)

  """
  write matrices with only sig genes. files are not used by this program,
  but potentially informative to the user
  """
  
  ScaledRef, ScaledMix = MatrixTools.RescaleRows(SigRef[1:], SigMix[1:], RowScaling)
 
  ScaledRef = [CTNames] + ScaledRef
  ScaledMix = [SampleNames] + ScaledMix 
  strDescr = "_".join(stringParams)

  if outFile == "None":
    SaveLocation =  "Output/" + "_".join(stringParams)
  elif outFile[-1] == "/":
    SaveLocation = outFile + "_".join(stringParams)
  else:
    SaveLocation = outFile
 
  #Write sigMatrix
  if SaveFiles != "None":
      MatrixTools.writeMatrix([CTNames] + SigRef, SaveLocation + "_SignatureGenes.tsv") 
  if SaveFiles == "All":
    #write scaled matrices
    MatrixTools.writeMatrix(ScaledRef, SaveLocation + "_ScaledRef.tsv")
    MatrixTools.writeMatrix(ScaledMix, SaveLocation + "_ScaledMix.tsv")

  Predictions = MatrixTools.PerformRegression(ScaledMix,ScaledRef)
  MatrixTools.writeMatrix(Predictions,SaveLocation + "_CTPredictions.tsv")
  if SaveFiles:
     print "Deconvolution Complete: Results located in: " + SaveLocation
     print "for visualization run \'Rscript VisualizePredictions.R " + SaveLocation + "_CTPredictions.tsv" +  "\'"
     print
  else:
     print "Deconvolution Complete: Results located in: " + SaveLocation.split("/")[-1] +"_Predictions.tsv"
     print "for visualization run \'Rscript VisualizePredictions.R " + SaveLocation.split("/")[-1] + "_Predictions.tsv"  "\'"
     print
     
  return

main()

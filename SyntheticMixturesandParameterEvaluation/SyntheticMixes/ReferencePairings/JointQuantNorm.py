#!/usr/bin/python
from sys import *
import os
import numpy as np

def main():
  myMat1 = readMatrix(argv[1])
  myMat2 = readMatrix(argv[2])
  outMat1, outMat2 = qNormMatrices(myMat1,myMat2)
  print argv[3]
  writeMatrix(outMat1, argv[3])
  writeMatrix(outMat2, argv[4])
def qNormMatrices(py_mat1, py_mat2):
  """
  quantile normalizes each column of targetMat and of mat1
  to the (overall) starting distribution of targetMat

  assumes first row and first column of both matrices
  are descriptions
  """
 
  mat1_temp = np.matrix(py_mat1[1:])
  mat1 = mat1_temp[:,1:].astype("float32")

  mat2_temp = np.matrix(py_mat2[1:])
  mat2 = mat2_temp[:,1:].astype("float32")

  targetVec1 = mat1.flatten().tolist()[0]
  targetVec2 = mat2.flatten().tolist()[0]
  targetVec = targetVec1 + targetVec2

  normedMat1 = qNorm_Matrix(mat1, targetVec)
  normedMat2 = qNorm_Matrix(mat2, targetVec)

  mat1_temp[:,1:] = normedMat1
  mat2_temp[:,1:] = normedMat2 
 

  return mat1_temp.tolist(), mat2_temp.tolist()

def qNorm_Matrix(matrix, targetVec):
  newMat = matrix.copy()
  for i in range(1,matrix.shape[1]):
    curVec = np.array(matrix[:,i].transpose())[0]
    normed = qNorm_useTarget( curVec, targetVec)
    newMat[:,i] = np.transpose([normed])
  return newMat

def qNorm_useTarget(data, target):
  """
  data is numpy array, target is python list
  """
  dOrder = np.argsort(np.array(data)).tolist()
  sortedTarget = sorted(target)
  newData = [0]*len(data)
  for index in dOrder:
    quantile = index/float(len(data)-1)
    corIndex = quantile*(len(target)-1)
    if corIndex.is_integer():
      newVal = sortedTarget[int(corIndex)]
    else:
      lower = sortedTarget[int(corIndex)]
      upper = sortedTarget[int(corIndex)+1]
      frac = corIndex-int(corIndex)
      newVal = upper*frac + lower*(1-frac)
      
    newData[dOrder[index]] = newVal
  return newData

def readMatrix(File):
  Matrix = []
  first = True
  for line in open(File, "r"):
    toAdd = line.strip().split("\t")
    if len(toAdd) == 1:
      toAdd = line.strip().split(",")
    if len(toAdd) == 1:
      toAdd = line.strip().split(" ")
    toAddTrimmed = [m.strip("\"") for m in toAdd] 
    if first:
      first = False
      toAdd = toAddTrimmed
    else:
      toAdd = [toAddTrimmed[0]] + [float(g) for g in toAddTrimmed[1:]]
    Matrix.append(toAdd)
  try:
    if len(Matrix[0]) == len(Matrix[1])-1:
      Matrix[0] = ["Gene"] + Matrix[0]        
  except:
    print Matrix
  return Matrix

def writeMatrix(Matrix, File):
  os.umask(000)
  fstream = open(File,"w+")
  for line in Matrix:
    fstream.write("\t".join([str(m) for m in line]))
    fstream.write("\n")
  fstream.close()
  return

def RescaleRows(Ref, Mix, power):
  Combined = [Ref[z] + Mix[z][1:] for z in range(len(Mix))]
  Scaled = Rescale_ZeroToOne(Combined, power)
  ScaledMix = []
  ScaledRef = []
  for m in range(len(Combined)):
    ScaledRef.append(Scaled[m][:len(Ref[0])])
    ScaledMix.append([Scaled[m][0]]+Scaled[m][len(Ref[0]):])
  return ScaledRef, ScaledMix
  
def Rescale_ZeroToOne(matrix, power):
  outMat = []
  for strVector in matrix:
    vector = []
    for strEl in strVector[1:]:
       el = float(strEl)
       vector.append(el)
    oldMin = min(vector)
    oldMax = max(vector)
    newMin = 0
    newMax = oldMax**power
    
    newVec = [str((m-oldMin)*newMax/(oldMax-oldMin)) for m in vector]
    

    outMat.append([strVector[0]] + newVec)
 
  return outMat

def removeDuplicates(matrix):
   outMatrix = []
   nameDict = {}
   for line in matrix:
     name = line[0]
     if name not in nameDict and len(name) > 0 and name != "NA":
       outMatrix.append(line)
       nameDict[name] = 0
   return outMatrix


def keepColumns(Matrix, colIndices):
  outMat = []
  for row in Matrix:
    outRow = []
    for i in range(len(row)):
      if i in colIndices:
        outRow.append(row[i])
    outMat.append(outRow)
  return outMat


def getBestCols(Matrix, numCols):
   #expects matrix of floats, except header
   #no row names
   """
   given a matrix of estimated proportions for each sample, returns
   the indices of the columns with the highest average values
   """
   outMat = []
   TotalValues = [0.0] * len(Matrix[1])
   for line in Matrix[1:]:
     for i in range(len(line)):
       TotalValues[i] += float(line[i])
   for line in Matrix:
     outLine = []
   SortedValues = sorted(TotalValues)[::-1]
   
   MaxIndices = []
   for MaxVal in SortedValues[:numCols]:
     MaxIndices.append(TotalValues.index(MaxVal))
     TotalValues[TotalValues.index(MaxVal)] = -1
   return MaxIndices

def getSharedRows(mat1, mat2):
  LookupD1 = {}
  for line in mat1:
    LookupD1[line[0].upper()] = line[1:]

  LookupD2 = {}
  for line in mat2:
    LookupD2[line[0].upper()] = line[1:]
  newMat1 = []

  for gname in sorted(LookupD1.keys()):
    if gname in LookupD2:
      newMat1.append([gname] + LookupD1[gname])

  newMat2 = []
  for gname in sorted(LookupD2.keys()):
    if gname in LookupD1:
      newMat2.append([gname] + LookupD2[gname])

  return newMat1, newMat2

def remove0s(matrix):
     newMat = []
     for line in matrix:
       total = 0.0
       for el in line:
          try:
            total += float(el)
          except:
            continue
       if total > 0.0:
         newMat.append(line)

     return newMat
main()
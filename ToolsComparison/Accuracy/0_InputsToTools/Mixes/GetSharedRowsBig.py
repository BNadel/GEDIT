#!/usr/bin/python
import sys
import os
import numpy as np

def main():
    mat1 = readMatrix(sys.argv[1])
    mat2 = readMatrix(sys.argv[2])

    newMat1, newMat2 = getSharedRows(mat1,mat2)
    newMat1 = [mat1[0]] + newMat1
    newMat1 = [mat2[0]] + newMat2
    writeMatrix(newMat1, sys.argv[3])
    writeMatrix(newMat2, sys.argv[4])

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
    try:
      line = "\t".join([line[0]] + [str(round(float(m),6)) for m in line[1:]])
    except:
      line = "\t".join([str(m) for m in line])
    
    fstream.write(line)
    fstream.write("\n")
  fstream.close()
  return

main()

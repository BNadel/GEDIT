import numpy as np
from MatrixTools import *
from scipy.optimize import nnls
from sys import *

def PerformRegression(pyMix,pyRef):

  npMix = np.array(pyMix)
  npRef = np.array(pyRef)
  CTNames = npRef[0,1:]
  npMix = npMix[1:,1:].astype("float32")
  npRef = npRef[1:,1:].astype("float32")
  Predictions = []
  Predictions.append(["Cell Type"] + CTNames.tolist())
  for i in range(npMix.shape[1]):
    curSample = npMix[:,i]
    fit = nnls(npRef,curSample)[0].tolist()
    normalized = [m/sum(fit) for m in fit]
    Predictions.append([pyMix[0][i+1]] + normalized)
  return Predictions

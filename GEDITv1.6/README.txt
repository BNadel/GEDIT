Author: Brian Nadel
Contact: brian.nadel@gmail.com -- please include "GEDIT" in the subject line

verified on R version 3.4.4 and python version 2.7

packages required in python:

  random
  numpy
  
in R:
  glmnet
  RColorBrewer
  gplots


Example Basic Command:
python GEDIT.py -mix mixtureFile.tsv -ref referenceFile.tsv -out outFile.tsv

This will print an R command, which you can execute to produce the final predictions

Leaving parameter values blank (as above) will use default values

NumSigs: default = 50
SigMethod: default = "Entropy"
RowScaling: default = 0.0
MinSigs = NumSigs

if the -out argument is left blank, GEDIT will write to a defualt file name
in the predictions/ directory (file name is composed of input file names and parameter choices)


You can also modify the parameters by adding arguments e.g.: 
python GEDIT.py -mix SampleMat1.csv -ref SampleMat2.csv -NumSigs 50 -SigMethod Entropy -RowScaling 0.0

Allowed values are:

NumSigs: 1-10,000
MinSigs: 1-NumSigs
RowScaling: 0.0-1.0
Method: [Intensity, Entorpy, Zscore, MeanRat, MeanDiff, fsRat, fsDiff]

methods can also be combined by comma seperating the terms (e.g. Entropy,fsRat).
This combines by rank-sum. Specifically, each gene is ranked by each metric selected. 
For each gene these ranks are summed, and genes with the lowest total are selected as signatures.

If an error is detected, the program may revert to default parameters

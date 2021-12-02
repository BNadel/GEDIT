Author: Brian Nadel
Contact: brian.nadel@gmail.com -- please include "GEDIT" in the subject line

verified on R version 3.4.4 and python version 2.7

packages required in python:

  random
  numpy
  
packages required in R:
  glmnet
  RColorBrewer
  gplots


GEDIT runs in two stages, first scripts in python, then in R
The "EasyRun.sh" script is provided for easy use, which automatically runs both stages

Example commands can be found in "SampleCommands.sh"

./EasyRun.sh -mix $MIXFILE -ref $REFFILE -out $OUTFILE
or just:
./EasyRun.sh -mix $MIXFILE -ref $REFFILE

Be sure to run in this current directory (wherever you have installed GEDIT), as GEDIT relies on local files paths



For advanced options, run the GEDIT.py script directly, followed by the R command generated:

python scripts/GEDIT.py -mix mixtureFile.tsv -ref referenceFile.tsv -out outFile.tsv
                   (-NumSigs 50 -MinSigs 50 -SigMethod Entropy -RowScaling 0.0)

This produces an R command, eg:

Rscript scripts/GLM_Decon.R /mnt/c/Users/brian/OneDrive/Desktop/GEDIT/FinalSoftware/GEDITv1.7/scripts/scratch/ImmuneCellMix.tsv_LM22.tsv_50_Entropy_0.2_ScaledMix.tsv /mnt/c/Users/brian/OneDrive/Desktop/GEDIT/FinalSoftware/GEDITv1.7/scripts/scratch/ImmuneCellMix.tsv_LM22.tsv_50_Entropy_0.2_ScaledRef.tsv examples/Outputs/ImmCM_Ref3_LM22.tsv


Parameters in parenthesis are optional, and values listed above are defaults.
Allowed ranges for these parameters are:

NumSigs: 1-10,000
MinSigs: 1-NumSigs
RowScaling: 0.0-1.0
Method: [Intensity, Entorpy, Zscore, MeanRat, MeanDiff, fsRat, fsDiff]

If the -out argument is left blank, GEDIT will write to a default file name in the predictions/ directory (file name is composed of input file names and parameter choices)

Methods can also be combined by comma seperating the terms (e.g. Entropy,fsRat).
This combines by rank-sum. Specifically, each gene is ranked by each metric selected. 
For each gene these ranks are summed, and genes with the lowest total are selected as signatures.

If invalid choices are designated, the program may revert to default parameters

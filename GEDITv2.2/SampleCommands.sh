#The most basic command is as follqws, and deposits the output file in the current working directory

python2 GEDIT2.py -mix ../ExampleMixtures/ImmuneCellMix.tsv -ref ../ReferenceMatrices/10XImmune.tsv

#one can also specify the output file

python2 GEDIT2.py -mix ../ExampleMixtures/ImmuneCellMix.tsv -ref ../ReferenceMatrices/10XImmune.tsv -outFile Output/ImmCM_Ref1_10x

#If desired, the VisualizePredictions.R script produces pdf and png images of the predictions

Rscript VisualizePredictions.R Output/ImmCM_Ref1_10x_CTPredictions.tsv

#Advanced setting are also available

#write additional output files. These are the intermediate "scaled" matrices used for the regression, and the matrix of Signature Genes
python2 GEDIT2.py -mix ../ExampleMixtures/ImmuneCellMix.tsv -ref ../ReferenceMatrices/10XImmune.tsv -outFile Output/ImmCM_Ref1_10x -SaveFiles yes

#use 45 signature genes per cell type instead of 50
python2 GEDIT2.py -mix ../ExampleMixtures/ImmuneCellMix.tsv -ref ../ReferenceMatrices/10XImmune.tsv -NumSigs 45 -outFile Output/ImmCM_Ref1_10x_45

#allow for more signature genes for some cell types than others (but a minumum of 30 for each, instead of the defualt 50
python2 GEDIT2.py -mix ../ExampleMixtures/ImmuneCellMix.tsv -ref ../ReferenceMatrices/ImmunoStates.tsv -MinSigs 30 -outFile Output/ImmCM_Ref2_ImmStat

#change the row scaling parameter from 0.0 to .2; this lessens the extent of the transformation
python2 GEDIT2.py -mix ../ExampleMixtures/ImmuneCellMix.tsv -ref ../ReferenceMatrices/LM22.tsv  -RowScaling .2 -outFile Output/ImmCM_Ref3_LM22

#select signature genes by meanRatio score
python2 GEDIT2.py -mix ../ExampleMixtures/SkinDiseases.tsv -ref ../ReferenceMatrices/BlueCodeV1.0.tsv -SigMethod MeanRat -outFile Output/Skin_Ref1_BC

#select signature genes using a hybrid meanRatio and Entropy score
python2 GEDIT2.py -mix ../ExampleMixtures/SkinDiseases.tsv -ref ../ReferenceMatrices/HPCA_Recommended.csv -SigMethod MeanRat,Entropy -outFile Output/Skin_Ref2_HPCA

#use multiple custom parameters
python2 GEDIT2.py -mix ../ExampleMixtures/SkinDiseases.tsv -ref ../ReferenceMatrices/SkinSignaturesV1.0.tsv -NumSigs 45 -SigMethod MeanRat -MinSigs 30 -RowScaling .2 -outFile Output/Skin_Ref3_Skin


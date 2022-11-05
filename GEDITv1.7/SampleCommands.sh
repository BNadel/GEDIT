#Use SimpleRun.sh to run GEDIT with default parameters. The input format is:

#./EasyRun.sh $MIXTURE $REFERENCE $OUTFILE

#e.g
./EasyRun.sh examples/Mixes/ImmuneCellMix.tsv ReferenceMatrices/Human/LM22.tsv
#If OUTPUTFILE is left blank, results will automatically write to the predictions/ directory with a name generated based on input files

#For advanced settings, run the python script directly. This will print to output an R command, which you can run to get the final results
#Examples:

#use 45 signature genes per cell type instead of 50
python scripts/GEDIT.py -mix ../Mixes/ImmuneCellMix.tsv -ref ReferenceMatrices/Human/10XImmune.tsv -NumSigs 45 -outFile examples/Outputs/ImmCM_Ref1_10x.tsv

#allow for more signature genes for some cell types than others (but a minumum of 30 for each, instead of the defualt 50
python scripts/GEDIT.py -mix ../Mixes/ImmuneCellMix.tsv -ref ReferenceMatrices/Human/ImmunoStates.csv -MinSigs 30 -outFile examples/Outputs/ImmCM_Ref2_ImmStat.tsv

#change the row scaling parameter from 0.0 to .2; this lessens the extent of the transformation
python scripts/GEDIT.py -mix ../Mixes/ImmuneCellMix.tsv -ref ReferenceMatrices/Human/LM22.tsv  -RowScaling .2 -outFile examples/Outputs/ImmCM_Ref3_LM22.tsv

#select signature genes by meanRatio score
python scripts/GEDIT.py -mix ../Mixes/SkinDiseases.tsv -ref ReferenceMatrices/Human/BlueCodeV1.0.tsv -SigMethod MeanRat -outFile examples/Outputs/Skin_Ref1_BC.tsv

#select signature genes using a hybrid meanRatio and Entropy score
python scripts/GEDIT.py -mix ../Mixes/SkinDiseases.tsv -ref ReferenceMatrices/Human/HPCAOrthogonalV1.0.csv -SigMethod MeanRat,Entropy -outFile examples/Outputs/Skin_Ref2_HPCA.tsv

#use multiple custom parameters
python scripts/GEDIT.py -mix ../Mixes/SkinDiseases.tsv -ref ReferenceMatrices/Human/SkinSignaturesV1.0.tsv -NumSigs 45 -SigMethod MeanRat -MinSigs 30 -RowScaling .2 -outFile examples/Outputs/Skin_Ref3_Skin.tsv

echo "Run these R commands above to produce final results for each example"

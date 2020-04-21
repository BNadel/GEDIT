python GEDIT.py -mix SampleMatrices/ImmuneCellMix/ImmuneCellMix.tsv -ref SampleMatrices/ImmuneCellMix/Ref1_10XImmune.tsv
python GEDIT.py -mix SampleMatrices/ImmuneCellMix/ImmuneCellMix.tsv -ref SampleMatrices/ImmuneCellMix/Ref1_10XImmune.tsv -outFile predictions/ImmCM_Ref1_10x.tsv
python GEDIT.py -mix SampleMatrices/ImmuneCellMix/ImmuneCellMix.tsv -ref SampleMatrices/ImmuneCellMix/Ref2_ImmunoStates.csv -NumSigs 45 -outFile predictions/ImmCM_Ref2_ImmStat.tsv
python GEDIT.py -mix SampleMatrices/ImmuneCellMix/ImmuneCellMix.tsv -ref SampleMatrices/ImmuneCellMix/Ref3_LM22.tsv  -MinSigs 30 -outFile predictions/ImmCM_Ref3_LM22.tsv
python GEDIT.py -mix SampleMatrices/SkinDiseases/SkinDiseases.tsv -ref SampleMatrices/SkinDiseases/Ref1_BlueCodeV1.0.csv -RowScaling .2 -outFile predictions/Skin_Ref1_BC.tsv
python GEDIT.py -mix SampleMatrices/SkinDiseases/SkinDiseases.tsv -ref SampleMatrices/SkinDiseases/Ref2_HPCAOrthogonalV1.0.csv -SigMethod MeanRat -outFile predictions/Skin_Ref2_HPCA.tsv
python GEDIT.py -mix SampleMatrices/SkinDiseases/SkinDiseases.tsv -ref SampleMatrices/SkinDiseases/Ref2_HPCAOrthogonalV1.0.csv -SigMethod MeanRat,Entropy -outFile predictions/Skin_Ref2_HPCA_MandEnt.tsv
python GEDIT.py -mix SampleMatrices/SkinDiseases/SkinDiseases.tsv -ref SampleMatrices/SkinDiseases/Ref3_SkinSignaturesV1.0.csv -NumSigs 45 -SigMethod MeanRat -MinSigs 30 -RowScaling .2 -outFile predictions/Skin_Ref3_Skin.tsv

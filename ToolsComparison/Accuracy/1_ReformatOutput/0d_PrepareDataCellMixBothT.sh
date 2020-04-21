shortinfix="CellMix"
longinfix="BothTCellMix"

for fname in A1_RawOutput/*$shortinfix*;
do newFname=$(basename $fname)
   echo "Running Command: python 1B_FormatPredictions.py $fname A2_TrueProps/Ascites.tsv $longinfix > B_ReformattedPredictions/$newFname;"
   python 1_FormatPredictions.py $fname A2_TrueProps/$longinfix.tsv $longinfix > B1_BothTCellMixReformatted/$newFname
   done
ls B1_BothTCellMixReformatted/*$shortinfix* > C_FileLists/FileList$longinfix.tsv

echo "Running: python 2_Unroll.py C_FileLists/FileList$longinfix.tsv A2_TrueProps/$longinfix.tsv > Unrolled$longinfix.tsv"
python 2_Unroll.py C_FileLists/FileList$longinfix.tsv A2_TrueProps/$longinfix.tsv > "Unrolled$longinfix.tsv";
cp Unrolled$longinfix.tsv ../2_MakeFigures/

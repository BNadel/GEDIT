infix="CellMix"

for fname in A1_RawOutput/*$infix*;
do newFname=$(basename $fname)
   echo "Running Command: python 1B_FormatPredictions.py $fname A2_TrueProps/Ascites.tsv $infix > B_ReformattedPredictions/$newFname;"
   python 1_FormatPredictions.py $fname A2_TrueProps/$infix.tsv $infix > B_ReformattedPredictions/$newFname
   done
ls B_ReformattedPredictions/*$infix* > C_FileLists/FileList$infix.tsv

echo "Running: python 2_Unroll.py C_FileLists/FileList$infix.tsv A2_TrueProps/$infix.tsv > Unrolled$infix.tsv"
python 2_Unroll.py C_FileLists/FileList$infix.tsv A2_TrueProps/$infix.tsv > "Unrolled$infix.tsv";
cp Unrolled$infix.tsv ../2_MakeFigures/

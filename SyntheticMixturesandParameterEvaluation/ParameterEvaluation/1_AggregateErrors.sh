ls AllErrors/* > C_AllFiles.txt
python A_CalcError.py C_AllFiles.txt 0 > Er_MinSigs.tsv
python A_CalcError.py C_AllFiles.txt 1 > Er_AvgSigs.tsv
python A_CalcError.py C_AllFiles.txt 2 > Er_SigMethod.tsv
python A_CalcError.py C_AllFiles.txt 3 > Er_RowScaling.tsv

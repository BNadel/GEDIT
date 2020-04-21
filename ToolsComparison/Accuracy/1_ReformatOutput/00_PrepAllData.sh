./0a_PrepareDataAscites.sh
./0b_PrepareDataCellMix.sh
./0c_PrepareDataHoek.sh
./0d_PrepareDataCellMixBothT.sh
cat UnrolledAscites.tsv UnrolledCellMix.tsv UnrolledHoek.tsv > UnrolledCombined.tsv
cp Unrolled* ../2_MakeFigures/

tsv=".tsv"
for mix in ../../Inputs/Mixes/*;
   do for ref in ../../Inputs/RefMats/*;
      do mixCore=$(basename $mix | cut -d "." -f 1)
      refCore=$(basename $ref | cut -d "." -f 1)
      sep=_
      outFile="../../Outputs/dtangle_$mixCore$sep$refCore"
      mixHead=$(echo $mixCore | head -c 7)
      refHead=$(echo $refCore | head -c 9)
      echo "./WrapperDtangle.sh $mix $ref $outFile$tsv";
      done; done

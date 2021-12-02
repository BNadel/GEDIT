echo "running python scripts/GEDIT.py -mix $1 -ref $2 -out $3"
a=$(python scripts/GEDIT.py -mix $1 -ref $2 -outFile $3)
echo $a
$a

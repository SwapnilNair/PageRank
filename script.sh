#!/bin/sh

CONVERGE=1

ITER=1

cat ./given_files/web-Google.txt | python3 t1_mapper.py | sort | python3 t1_reducer.py ./given_files/w.txt > out.txt

while [ "$CONVERGE" -ne 0 ]
do

echo "############################# ITERATION $ITER #############################"


touch ./given_files/w1.txt

cat out.txt | python3 t2_mapper.py ./given_files/w.txt ./given_files/page_embeddings.json | sort -n | python3 t2_reducer.py > w1.txt

cat ./given_files/w1.txt
CONVERGE=$(python3 ./given_files/check_conv.py $ITER>&1)
ITER=$((ITER+1))

echo $CONVERGE

mv ./given_files/w1.txt ./given_files/w.txt

done
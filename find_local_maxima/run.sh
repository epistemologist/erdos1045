#!/bin/bash

for i in $(seq 5 2 40); do
#	echo $i, $(($i+1))
	python3 find_minima.py "$i" &
	python3 find_minima.py "$((i+1))" &
	wait
done

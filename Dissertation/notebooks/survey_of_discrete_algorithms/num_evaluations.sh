#!/bin/bash

while true; do
	n=$(cat evaluations/*.dat | grep -c "N")
	now=$(date +"%T")
	echo -ne "\033[1K\r$now   $n"
	sleep 1
done
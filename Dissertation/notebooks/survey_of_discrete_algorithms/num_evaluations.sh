#!/bin/bash

while true; do
	n=$(wc -l evaluations/*.dat | grep total)
	now=$(date +"%T")
	echo -ne "\033[1K\r$now$n"
	sleep 1
done
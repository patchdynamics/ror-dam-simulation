#!/bin/bash
#./scripts/clear.sh
anneal=(.5 .3 .1)
echo $anneal
set -e
for epsilon in $anneal
do
	for n in $(seq 25)
	do
		echo $n	
		echo $epsilon
		echo '.'
		python runSimulation.py -e $epsilon --dams 1  --year 2005 -a KNN #> /dev/null
		echo '.'
		python runSimulation.py -e $epsilon --dams 1  --year 2006 -a KNN #> /dev/null
		echo '.'
		python runSimulation.py -e $epsilon --dams 1 --year 2007 -a KNN #> /dev/null
		echo '.'
		python runSimulation.py -e $epsilon --dams 1 --year 2008 -a KNN #> /dev/null
		echo '.'
		python runSimulation.py -e $epsilon --dams 1 --year 2009 -a KNN #> /dev/null
	done
done

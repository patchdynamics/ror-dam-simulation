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
		./runSimulation.py -e $epsilon --dams 1  --year 2005 #> /dev/null
		echo '.'
		./runSimulation.py -e $epsilon --dams 1  --year 2006 #> /dev/null
		echo '.'
		./runSimulation.py -e $epsilon --dams 1 --year 2007 #> /dev/null
		echo '.'
		./runSimulation.py -e $epsilon --dams 1 --year 2008 #> /dev/null
		echo '.'
		./runSimulation.py -e $epsilon --dams 1 --year 2009 #> /dev/null
	done
done

#!/bin/bash
#./scripts/clear.sh
anneal=(.5 .4 .4 .3 .3 .2 .2 .1 .1 .1 .05 .05 .05 .01 .01 .01 0 0 0)
anneal=(.3 .3 .2 .2 .1 .1 .1 .05 .05 .05 .01 .01 .01 0 0 0)
anneal=(0 0 0)
set -e
for epsilon in "${anneal[@]}"
do
	for n in $(seq 25)
	do
		echo $n	
		echo $epsilon
		#echo '.'
		#./runSimulation.py -e $epsilon --dams 1  --year 2005 #> /dev/null
		#echo '.'
		#./runSimulation.py -e $epsilon --dams 1  --year 2006 #> /dev/null
		echo '.'
		./runSimulation.py -e $epsilon --dams 1 --year 2007 -a Linear #> /dev/null
		#echo '.'
		#./runSimulation.py -e $epsilon --dams 1 --year 2008 #> /dev/null
		#echo '.'
		#./runSimulation.py -e $epsilon --dams 1 --year 2009 #> /dev/null
	done
done

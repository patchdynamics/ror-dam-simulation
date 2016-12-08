#!/bin/bash
#./scripts/clear.sh
anneal=(.5 .4 .4 .3 .3 .2 .2 .1 .1 .1 .05 .05 .05 .01 .01 .01 0 0 0)
anneal=(.2 .2 .1 .1 .1 .05 .05 .05 .01 .01 .01 0 0 0)
anneal=(.1 0)
#anneal=(.2 .2 .1 .1 .1 .05 .05 .05 .01 .01 .01 0 0 0)
#anneal=(0 0 0)
>>>>>>> Stashed changes
echo $anneal
set -e
for epsilon in "${anneal[@]}"
do
	for n in $(seq 25)
	do
		echo $n	
		echo $epsilon
		echo '.'
		#python runSimulation.py -e $epsilon --dams 1  --year 2005 -a Lookup #> /dev/null
		echo '.'
		#python runSimulation.py -e $epsilon --dams 1  --year 2006 -a Lookup #> /dev/null
		echo '.'
		python runSimulation.py -e $epsilon --dams 1 --year 2007 -a Lookup #> /dev/null
		echo '.'
		#python runSimulation.py -e $epsilon --dams 1 --year 2008 -a Lookup #> /dev/null
		echo '.'
		#python runSimulation.py -e $epsilon --dams 1 --year 2009 -a Lookup #> /dev/null
	done
done

#!/bin/bash
#./scripts/clear.sh
set -e
echo '.'
./runSimulation.py -t --dams 1  --year 2010 > /dev/null
echo '.'
./runSimulation.py -t --dams 1  --year 2011 > /dev/null
echo '.'
./runSimulation.py -t --dams 1 --year 2012 > /dev/null
echo '.'
./runSimulation.py -t --dams 1 --year 2013 > /dev/null
echo '.'
./runSimulation.py -t --dams 1 --year 2014 > /dev/null
echo '.'
./runSimulation.py -t --dams 1 --year 2015 > /dev/null

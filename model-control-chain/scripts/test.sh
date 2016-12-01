#!/bin/bash
set -e
echo '.'
./runSimulation.py -t --dams 1  --year 2005 > /dev/null
echo '.'
./runSimulation.py -t --dams 1  --year 2006 > /dev/null
echo '.'
./runSimulation.py -t --dams 1 --year 2007 > /dev/null
echo '.'
./runSimulation.py -t --dams 1 --year 2008 > /dev/null
echo '.'
./runSimulation.py -t --dams 1 --year 2009 > /dev/null

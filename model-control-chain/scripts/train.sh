#!/bin/bash
./scripts/clear.sh
echo '.'
./runSimulation.py  --year 2005 > /dev/null
echo '.'
./runSimulation.py  --year 2006 > /dev/null
echo '.'
./runSimulation.py  --year 2007 > /dev/null
echo '.'
./runSimulation.py  --year 2008 > /dev/null
echo '.'
./runSimulation.py  --year 2009 > /dev/null

#!/bin/bash
set -e
head -93 wb1/inputs/QIN2007.npt > wb1/qin.npt
tail -275 wb1/inputs/QIN2005.npt >> wb1/qin.npt
python runSimulation.py -t --dams 1  --year 2005 -a Lookup

head -93 wb1/inputs/QIN2007.npt > wb1/qin.npt
tail -275 wb1/inputs/QIN2006.npt >> wb1/qin.npt
python runSimulation.py -t --dams 1  --year 2006 -a Lookup

head -93 wb1/inputs/QIN2007.npt > wb1/qin.npt
tail -276 wb1/inputs/QIN2008.npt >> wb1/qin.npt
python runSimulation.py -t --dams 1 --year 2008 -a Lookup

head -93 wb1/inputs/QIN2007.npt > wb1/qin.npt
tail -275 wb1/inputs/QIN2009.npt >> wb1/qin.npt
python runSimulation.py -t --dams 1 --year 2009 -a Lookup

head -93 wb1/inputs/QIN2007.npt > wb1/qin.npt
tail -275 wb1/inputs/QIN2010.npt >> wb1/qin.npt
python runSimulation.py -t --dams 1 --year 2010 -a Lookup

head -93 wb1/inputs/QIN2007.npt > wb1/qin.npt
tail -275 wb1/inputs/QIN2011.npt >> wb1/qin.npt
python runSimulation.py -t --dams 1 --year 2011 -a Lookup

head -93 wb1/inputs/QIN2007.npt > wb1/qin.npt
tail -276 wb1/inputs/QIN2012.npt >> wb1/qin.npt
python runSimulation.py -t --dams 1 --year 2012 -a Lookup

head -93 wb1/inputs/QIN2007.npt > wb1/qin.npt
tail -275 wb1/inputs/QIN2013.npt >> wb1/qin.npt
python runSimulation.py -t --dams 1 --year 2013 -a Lookup

head -93 wb1/inputs/QIN2007.npt > wb1/qin.npt
tail -275 wb1/inputs/QIN2014.npt >> wb1/qin.npt
python runSimulation.py -t --dams 1 --year 2014 -a Lookup

head -93 wb1/inputs/QIN2007.npt > wb1/qin.npt
tail -275 wb1/inputs/QIN2015.npt >> wb1/qin.npt
python runSimulation.py -t --dams 1 --year 2015 -a Lookup
#!/bin/bash
module load Python/2.7.11
export PYTHONPATH=$PYTHONPATH:/home/mshultz/virtualenvs/py2.7/lib/python2.7/
python --version
set -e
while true
do
  python runSimulation.py -e 0 --dams 1 --year 2007 -a Lookup
done

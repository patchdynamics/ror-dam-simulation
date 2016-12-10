#!/bin/bash
set -e
while true
do
  python runSimulation.py -e 0 --dams 1 --year 2007 -a KNN
done

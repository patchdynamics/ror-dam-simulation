#!/bin/bash
set -e

# year and day are specified somewhere
YEAR=2015
DAY=100

run.model()
{
	# VERIFY restart files should already be in place, no need to copy
	# cp outputs/$1/$YEAR/$DAY/rso$DAY.opt rsi.npt
	# cp outputs/$1/$YEAR/$DAY/spr.opt spr.opt # looks like it wants to keep adding to this
	cd $1
	wine ../../../CE-QUAL-W2-v372/executables/w2\ model/w2_ivf32_v372.exe
	cd ../
	#mkdir -p outputs/$1/$YEAR/$DAY
	#cp *.opt outputs/$1/$YEAR/$DAY
	if [ -n $2 ]
	then
		cut -c 1-16 $1/qwo_34.opt > $2/qin.npt
		cut -c 1-16 $1/two_34.opt > $2/tin.npt
	fi
}

# only when starting
cp wb1/inputs/QIN$YEAR.npt wb1/qin.npt
cp wb1/inputs/TIN$YEAR.npt wb1/tin.npt
#each day
cp wb1/inputs/control/daily.npt wb1/w2_con.npt
cp wb2/inputs/control/daily.npt wb2/w2_con.npt
# TODO copy in the spin ups
# TODO generate spin ups for all years and water bodies
cp wb1/inputs/spinup/$YEAR/*.opt wb1  # testing spinup, appears to want ALL the opt files 
cp wb2/inputs/spinup/$YEAR/*.opt wb2  # testing spinup, appears to want ALL the opt files 
run.model wb1 wb2
run.model wb2 wb3
#run.model wb3 wb4
#run.model wb4

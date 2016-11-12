#!/bin/bash
set -e

# year and day are specified somewhere
YEAR=2015
DAY=100

run.model()
{
	cd $1
	wine ../../../CE-QUAL-W2-v372/executables/w2\ model/w2_ivf32_v372.exe
	cd ../
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
cp wb1/inputs/control/year.npt wb1/w2_con.npt
cp wb2/inputs/control/year.npt wb2/w2_con.npt
cp wb3/inputs/control/year.npt wb3/w2_con.npt
cp wb4/inputs/control/year.npt wb4/w2_con.npt

cp wb1/inputs/spinup/$YEAR/*.opt wb1 
cp wb2/inputs/spinup/$YEAR/*.opt wb2 
cp wb3/inputs/spinup/$YEAR/*.opt wb3
cp wb4/inputs/spinup/$YEAR/*.opt wb4 

cp wb1/inputs/QOUT$YEAR.npt wb1/qot_br1.npt
run.model wb1 wb2
run.model wb2 wb3
run.model wb3 wb4
run.model wb4

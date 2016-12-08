#!/bin/bash
YEAR=$1

cd wb1
set +e
\rm *.opt
set -e
sed s/%%%%/$YEAR/ inputs/control/spinup90.npt > w2_con.npt
cp inputs/TIN$YEAR.npt tin.npt
cp inputs/QIN$YEAR.npt qin.npt
cp inputs/qout_year/QOUT$YEAR.npt qot_br1.npt
cp inputs/met$YEAR.npt met.npt
#../../bin/cequalw2.v371.mac.fast .
wine ../../bin/w2_ivf32_v372.exe
mkdir -p inputs/spinup/$YEAR
cp *.opt inputs/spinup/$YEAR
cp qin.npt inputs/spinup/$YEAR
cp tin.npt inputs/spinup/$YEAR

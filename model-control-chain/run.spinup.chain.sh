YEAR=$1

cd wb1
set +e
\rm *.opt
set -e
sed s/%%%%/$YEAR/ inputs/control/spinup.npt > w2_con.npt
cp inputs/TIN$YEAR.npt tin.npt
cp inputs/QIN$YEAR.npt qin.npt
cp inputs/QOUT$YEAR.npt qot_br1.npt
cp inputs/met$YEAR.npt met.npt
#../../bin/cequalw2.v371.mac.fast .
wine ../../bin/w2_ivf32_v372.exe
cut -c 1-16 qwo_34.opt > ../wb2/qin.npt   # process q and t output into input for next water body
cut -c 1-16 two_34.opt > ../wb2/tin.npt
mkdir -p inputs/spinup/$YEAR
mv rso*.opt inputs/spinup/$YEAR/other-restart/
cp *.opt inputs/spinup/$YEAR
cp qin.npt inputs/spinup/$YEAR
cp tin.npt inputs/spinup/$YEAR
cp inputs/spinup/$YEAR/other-restart/rso60.opt inputs/spinup/$YEAR

cd ../wb2
pwd
set +e
\rm *.opt
set -e
sed s/%%%%/$YEAR/ inputs/control/spinup.npt > w2_con.npt
cp inputs/QOUT$YEAR.npt qot_br1.npt
cp inputs/met$YEAR.npt met.npt
#../../bin/cequalw2.v371.mac.fast .
wine ../../bin/w2_ivf32_v372.exe
cut -c 1-16 qwo_34.opt > ../wb3/qin.npt   # process q and t output into input for next water body
cut -c 1-16 two_34.opt > ../wb3/tin.npt
mkdir -p inputs/spinup/$YEAR
mv rso*.opt inputs/spinup/$YEAR/other-restart/
cp *.opt inputs/spinup/$YEAR
cp qin.npt inputs/spinup/$YEAR
cp tin.npt inputs/spinup/$YEAR
cp inputs/spinup/$YEAR/other-restart/rso60.opt inputs/spinup/$YEAR


cd ../wb3
pwd
set +e
\rm *.opt
set -e
sed s/%%%%/$YEAR/ inputs/control/spinup.npt > w2_con.npt
cp inputs/QOUT$YEAR.npt qot_br1.npt
cp inputs/met$YEAR.npt met.npt
#../../bin/cequalw2.v371.mac.fast .
wine ../../bin/w2_ivf32_v372.exe
cut -c 1-16 qwo_34.opt > ../wb4/qin.npt   # process q and t output into input for next water body
cut -c 1-16 two_34.opt > ../wb4/tin.npt
mkdir -p inputs/spinup/$YEAR
mv rso*.opt inputs/spinup/$YEAR/other-restart/
cp *.opt inputs/spinup/$YEAR
cp qin.npt inputs/spinup/$YEAR
cp tin.npt inputs/spinup/$YEAR
cp inputs/spinup/$YEAR/other-restart/rso60.opt inputs/spinup/$YEAR


cd ../wb4
set +e
\rm *.opt
set -e
sed s/%%%%/$YEAR/ inputs/control/spinup.npt > w2_con.npt
cp inputs/QOUT$YEAR.npt qot_br1.npt
cp inputs/met$YEAR.npt met.npt
#../../bin/cequalw2.v371.mac.fast .
wine ../../bin/w2_ivf32_v372.exe
mkdir -p inputs/spinup/$YEAR
mv rso*.opt inputs/spinup/$YEAR/other-restart/
cp *.opt inputs/spinup/$YEAR
cp qin.npt inputs/spinup/$YEAR
cp tin.npt inputs/spinup/$YEAR
cp inputs/spinup/$YEAR/other-restart/rso60.opt inputs/spinup/$YEAR
cd ../



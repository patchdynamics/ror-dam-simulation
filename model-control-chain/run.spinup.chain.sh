cd wb1
set +e
\rm *.opt
set -e
cp inputs/control/2015spinup.npt w2_con.npt
cp inputs/TIN2015.npt tin.npt
cp inputs/QIN2015.npt qin.npt
cp inputs/QOUT2015.npt qot_br1.npt
wine ../../bin/w2_ivf32_v372.exe
cut -c 1-16 qwo_34.opt > ../wb2/qin.npt   # process q and t output into input for next water body
cut -c 1-16 two_34.opt > ../wb2/tin.npt
cp *.opt inputs/spinup/2015


cd ../wb2
cp inputs/control/2015spinup.npt w2_con.npt
set +e
\rm *.opt
set -e
cp inputs/QOUT2015.npt qot_br1.npt
wine ../../bin/w2_ivf32_v372.exe
cut -c 1-16 qwo_34.opt > ../wb3/qin.npt   # process q and t output into input for next water body
cut -c 1-16 two_34.opt > ../wb3/tin.npt
cp *.opt inputs/spinup/2015


cd ../wb3
cp inputs/control/2015spinup.npt w2_con.npt
set +e
\rm *.opt
set -e
cp inputs/QOUT2015.npt qot_br1.npt
wine ../../bin/w2_ivf32_v372.exe
cut -c 1-16 qwo_34.opt > ../wb4/qin.npt   # process q and t output into input for next water body
cut -c 1-16 two_34.opt > ../wb4/tin.npt
cp *.opt inputs/spinup/2015


cd ../wb4
cp inputs/control/2015spinup.npt w2_con.npt
set +e
\rm *.opt
set -e
cp inputs/QOUT2015.npt qot_br1.npt
wine ../../bin/w2_ivf32_v372.exe
cp *.opt inputs/spinup/2015
cd ../



#!/bin/bash
set -e
cp inputs/control/year.npt w2_con.npt
cp inputs/TIN2015.npt tin.npt
cp inputs/QIN2015.npt qin.npt
cp inputs/QOUT2015.npt qot_br1.npt
wine ../../bin/w2_ivf32_v372.exe

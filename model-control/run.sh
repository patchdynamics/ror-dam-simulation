# year and day are specified somewhere
YEAR=2015
DAY=100

run.model()
{
	wine ../../CE-QUAL-W2-v372/executables/w2\ model/w2_ivf32_v372.exe 
	mkdir -p outputs/$1/$YEAR/$DAY
	cp *.opt outputs/$1/$YEAR/$DAY
	cut -c 1-16 qwo_34.opt > qin.npt   # process q and t output into input for next water body
	cut -c 1-16 two_34.opt > tin.npt
	rm *.opt
}

cp inputs/QIN$YEAR.npt qin.npt
cp inputs/TIN$YEAR.npt tin.npt
run.model wb1
run.model wb2
run.model wb3
run.model wb4

# year and day are specified somewhere
YEAR=2015
DAY=100

cp inputs/QIN$YEAR.npt qin.npt
cp inputs/TIN$YEAR.npt tin.npt

	cp outputs/wb1/$YEAR/$DAY/rso$DAY.opt rsi.npt
	wine ../../CE-QUAL-W2-v372/executables/w2\ model/w2_ivf32_v372.exe 
	mkdir -p outputs/wb1/$YEAR/$DAY
	cp *.opt outputs/wb1/$YEAR/$DAY
	cut -c 1-16 qwo_34.opt > qin.npt   # process q and t output into input for next water body
	cut -c 1-16 two_34.opt > tin.npt
	rm *.opt



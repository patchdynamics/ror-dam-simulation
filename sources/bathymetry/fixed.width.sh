cp bth.original.npt bth.processing
perl -p -i -e "s/(\s+[0-9]+\.[0-9]+)/sprintf ' %7.2f', \$1/eg" bth.processing
perl -p -i -e "s/(\s+\.[0-9]+)/sprintf ' %7.2f', \$1/eg" bth.processing  
mv bth.processing bth.npt

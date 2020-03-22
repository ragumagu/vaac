#!/bin/bash

cp $1/recordings/* $1/working/
cp -r en-us $1/working/
cp $1/$1_lm/* $1/working

python trainer.py --modelname $1

cd $1/working

sphinx_lm_convert -i $1.lm -o $1.lm.bin

sphinx_fe -argfile ./en-us/feat.params -samprate 16000 -c $1.fileids -di . -do . -ei wav -eo mfc -mswav yes

cp /usr/local/libexec/sphinxtrain/bw .
cp /usr/local/libexec/sphinxtrain/mllr_solve .

./bw  -hmmdir en-us  -moddeffn en-us/mdef  -ts2cbfn .cont.  -feat 1s_c_d_dd  -cmn current  -agc none  -dictfn $1.dic  -ctlfn $1.fileids  -lsnfn $1.transcription  -accumdir .

./mllr_solve -meanfn en-us/means -varfn en-us/variances -outmllrfn mllr_matrix -accumdir . 

# Use the following for map adapt.
# cp /usr/local/libexec/sphinxtrain/map_adapt .
# cp -a en-us en-us-adapt

#./map_adapt \
#    -moddeffn en-us/mdef \
#    -ts2cbfn .cont. \
#    -meanfn en-us/means \
#    -varfn en-us/variances \
#    -mixwfn en-us/mixture_weights \
#    -tmatfn en-us/transition_matrices \
#    -accumdir . \
#    -mapmeanfn en-us-adapt/means \
#    -mapvarfn en-us-adapt/variances \
#    -mapmixwfn en-us-adapt/mixture_weights \
#    -maptmatfn en-us-adapt/transition_matrices


!#/bin/bash

sphinx_fe -argfile ./data/en-us/feat.params -samprate 16000 -c ./data/pocketsphinx_files/recordings.fileids -di . -do . -ei wav -eo mfc -mswav yes

./bw  -hmmdir ./data/en-us  -moddeffn ./data/en-us/mdef  -ts2cbfn .cont.  -feat 1s_c_d_dd  -cmn current  -agc none  -dictfn ./data/pocketsphinx_files/vaac_lm/vaac.dic  -ctlfn ./data/pocketsphinx_files/recordings.fileids  -lsnfn ./data/pocketsphinx_files/recordings.transcription  -accumdir .

./mllr_solve -meanfn ./data/en-us/means -varfn ./data/en-us/variances -outmllrfn mllr_matrix -accumdir .

pocketsphinx_continuous -hmm ./data/en-us -lm ./data/pocketsphinx_files/vaac_lm/vaac.lm.bin -dict ./data/pocketsphinx_files/vaac_lm/vaac.dic -inmic yes
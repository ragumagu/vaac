#!/bin/bash
pocketsphinx_continuous -hmm $1/working/en-us -lm $1/working/$1.lm.bin -dict $1/working/$1.dic -inmic yes
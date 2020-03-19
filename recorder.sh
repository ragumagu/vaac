#!/bin/bash
arecord -f S16_LE -d $1 -r 16000 test.wav

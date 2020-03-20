#!/bin/bash
arecord -f S16_LE -d 5 -r 16000 /tmp/test.wav
aplay /tmp/test.wav

#!/bin/bash
mkdir $1
mkdir $1/recordings
mkdir $1/working
echo "{\"n\":0,\"i\":0}" >> $1/recording_progress.json

echo "Building directory tree:"
tree $1
echo "Done."
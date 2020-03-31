#!/bin/bash
echo "Extracting files..."
var="$2/$2_lm"
echo $var
mkdir -p "$2/$2_lm"
tar --extract --file $1 -C $2/$2_lm

echo "Renaming files..."
for x in $2/$2_lm/*; do mv "$x" "$2/$2_lm/$2.${x##*.}"; done

echo "Extracting phones..."
python3 phones_extractor.py --modeldir $2

echo "Copying .filler file..."
cp "./model.filler" "$2/$2_lm/$2.filler"
echo "Done"

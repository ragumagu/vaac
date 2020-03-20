#!/bin/bash
echo "Extracting files..."
var="$2/$2_lm"
echo $var
mkdir -p "$2/$2_lm"
tar --extract --file $1 -C $2/$2_lm

echo "Renaming files..."
for x in $2/$2_lm/*; do mv "$x" "$2/$2_lm/$2.${x##*.}"; done

echo "Done"
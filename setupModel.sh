#!/bin/bash
modeldir="vaac_model"
for ARGUMENT in "$@"
do
    KEY=$(echo $ARGUMENT | cut -f1 -d=)
    VALUE=$(echo $ARGUMENT | cut -f2 -d=)

    case "$KEY" in
            tarfile)  tarfile=${VALUE} ;;
            *)
    esac
done

echo "Extracting from" $tarfile
mkdir -p "$modeldir/etc"
tar --extract --file $tarfile -C "$modeldir/etc"

echo "Renaming files..."
for x in "./$modeldir/etc"/*
do
    mv "$x" "$modeldir/etc/$modeldir.${x##*.}"
done

echo "Converting lm file to lm.DMP file"
sphinx_lm_convert -i "$modeldir/etc/$modeldir.lm" -o "$modeldir/etc/$modeldir.lm.DMP"
rm "$modeldir/etc/$modeldir.lm"

echo "Extracting phones..."
while IFS="" read -r line || [ -n "$line" ]
do
    i=0
    for word in $line; do
        if [[ $i -eq 1 ]]; then # skips first word
            echo $word >> "$modeldir/etc/$modeldir.phone"
        fi
        i=1
    done
done < "$modeldir/etc/$modeldir.dic"
sort -u -o "$modeldir/etc/$modeldir.phone" "$modeldir/etc/$modeldir.phone"

echo "Copying .filler file..."
cp "data/model.filler" "$modeldir/etc/$modeldir.filler"

echo "Generating fileids and transcription"
python3 vaac_code/generate_fileids.py

echo "Done"



#!/bin/bash

if [[ "$1" != "" ]]; then
    DIR="$1"
else
    DIR="bootstrap"
fi

cp scss/* "$DIR/scss/"
cd $DIR
grunt dist

rm -rf ../dist/
mv dist/ ..

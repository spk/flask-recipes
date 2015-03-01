#!/usr/bin/env sh
set -e

mkdir -p recipes

for i in $(seq -w 1 110)
do
    wget "http://dsquirrel.tripod.com/xmlzips/RecipeMLArchive00${i}.zip" -O "${i}.zip"
done

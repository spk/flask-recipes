#!/usr/bin/env sh
set -e

DEST_DIR="recipes"
mkdir -p "${DEST_DIR}"

for i in $(seq -w 1 110)
do
    wget -c "http://dsquirrel.tripod.com/xmlzips/RecipeMLArchive00${i}.zip" \
        -O "${DEST_DIR}/${i}.zip"
done

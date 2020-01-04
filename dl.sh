#!/bin/bash

FILE="build.zip"
BUILD_DIR="build"
FILEID='1xP1AKzJdMISnkGWGNKUm_EfJvjCurgmW'
URL="https://docs.google.com/uc?export=download&id=${FILEID}"

if [ ! -f "$FILE" ]; then
    wget --no-check-certificate -r $URL -O $FILE 1>/dev/null 2>&1
fi

if [ ! -d "$BUILD_DIR" ]; then
    unzip $FILE -d $BUILD_DIR 1>/dev/null 2>&1
fi

#!/bin/sh
set -e
ffmpeg -i "$1" -vn "$1".wav

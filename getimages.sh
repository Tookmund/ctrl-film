#!/bin/sh
ffmpeg -i "$1" -vf "select=not(mod(n\,100))" -vsync vfr img_%03d.png
ffmpeg -i "$1" 2>&1 | sed -n "s/.*, \(.*\) fps.*/\1/p"

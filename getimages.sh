#!/bin/sh
ffmpeg -i "$1" -vf "select=not(mod(n\,100))" -vsync vfr img_%03d.png 2>&1 | sed -n "s/.*, \(.*\) fps.*/\1/p"

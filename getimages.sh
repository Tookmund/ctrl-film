#!/bin/sh
ffmpeg -i "$1" -vf "select=not(mod(n\,100))" -vsync vfr img_%03d.png

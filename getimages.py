#!/usr/bin/env python
import sys
import ffmpeg

(
        ffmpeg
        .input(sys.argv[1])
        .filter('select', 'not(mod(n,30))')
        .output('img_%03d.png')
        .run()
)

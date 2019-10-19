#!/usr/bin/env python
import os
import sys
import pytesseract

for pic in os.listdir(sys.argv[1]):
    print(pytesseract.image_to_string(sys.argv[1]+'/'+pic))

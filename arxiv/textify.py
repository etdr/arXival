#!/usr/bin/python

import subprocess
import os
import os.path as path


for root, dirs, files in os.walk("."):
  files = list(files)
  for filename in files:
    fn, ext = path.splitext(filename)
    print(ext)
    if ext == '.pdf':
      if fn+'.txt' in files:
        print('skipping',fn)
        continue
      subprocess.run(['pdftotext',filename,fn+'.txt'])
      subprocess.run(['pdftotext','-layout',filename,fn+'_layout.txt'])
    
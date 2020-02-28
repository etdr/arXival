
import re

newline_re = re.compile('\n')

# import list of English words into set
words = set()
with open('/home/winfield/d/arXival/words.txt','rt') as f:
    for l in f.readlines():
        words.add(newline_re.sub('',l).lower())
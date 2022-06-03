import re

def grep(something, lines):
    for line in lines:
        if re.search(str( something ), line):
            return line

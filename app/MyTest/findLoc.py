__author__ = 'Hao'
# visit all subdir and find log related to Location

import os
import re

def visit(arg, dirname, files):
    global counter, subcounter
    counter += 1
    for filename in files:
        if re.search('\.log', filename):
            print filename
            try:
                file = open(dirname + '/' + filename, 'r')
            except IOError:
                continue
            lines = file.readlines()
            for line in lines:
                if re.search('.*?Location.*?', line):
                    print dirname
                    subcounter += 1
                    os.system('cp -r ' + dirname + ' /home/hao/Documents/Loc')
                    break
            break


counter = 0
subcounter = 0
os.path.walk('/media/hao/Hitachi/BaiduApks/software/504/4/LOC/data', visit, None)
print counter
print subcounter
print float(subcounter) / float(counter)

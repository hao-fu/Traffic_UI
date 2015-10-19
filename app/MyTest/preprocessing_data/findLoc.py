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
                    os.system('cp -r ' + dirname + ' /home/hao/Documents/Loc/social')
                    break
            break


counter = 0
subcounter = 0
#dir = '/home/hao/Documents/NEWS_AND_MAGAZINES_LOC/'
#dir = '/media/hao/Hitachi/BaiduApks/software/504/6/LOC/data'
dir = '/media/hao/Hitachi/Apps/SOCIAL/LOC/data'
os.path.walk(dir, visit, None)
print counter
print subcounter
print float(subcounter) / float(counter)

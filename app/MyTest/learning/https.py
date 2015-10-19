__author__ = 'hao'
import os
import re

def visit(arg, dirname, files):
    for filename in files:
        #print dirname
        if re.search('-.*?\.log', filename) and not re.search('UI', filename):
            #flag = True
            log = open(dirname + '/' + filename, 'r')
            lines = log.readlines()
            for line in lines:
                if re.search('Location', line) and re.search('SSL', line):
                    app = line.split(': ')[1].split(',')[0]
                        #and not re.search('com.google.process.gapps', line):
                    if app not in applist:
                        applist.append(app)
                        print dirname
                        #flag = False
                        if re.search('/0', dirname):
                            applist_0.append(app)

                        else:
                            applist_1.append(app)
                    ip = line.split(',')[1]
                    if ip not in IP:
                        IP.append(ip)
                    print line


applist = []
applist_0 = []
applist_1 = []
IP = []
dir = '/home/hao/Documents/Ground'
os.path.walk(dir, visit, None)
print applist
print len(applist), len(applist_0), len(applist_1)
print len(IP)
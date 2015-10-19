import os
import re

appdir = '/media/hao/Hitachi/BaiduApks/software/504/'
filelist = os.listdir(appdir) # list files at current dir
#filename = str(id) + '.html'
counter = 0
dir = 5
for file in filelist:
	if re.search('\.apk', file):
		print file
		if counter % 2000 == 0:
			dir += 1
			os.system('mkdir ' + appdir + str(dir))
		os.system('mv ' + appdir + file + ' ' + appdir + str(dir))
		counter += 1


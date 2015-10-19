# -*- coding: utf-8 -*-
__author__ = 'hao'

import os
import re

def visit(arg, dirname, files):
    appname = dirname.split('/')
    appname = appname[len(appname) - 1]
    if appname in already_apps:
        index = already_apps.index(appname)
        os.popen('cp -r ' + dirname + ' ' + already_apps_dir[index])
        result = os.popen('rm -rf ' + dirname)
        print result

def already_app_list(arg, dirname, files):
    appname = dirname.split('/')
    appname = appname[len(appname) - 1]
    if appname not in already_apps and appname:
        already_apps.append(appname)
        already_apps_dir.append(dirname)

already_dir = '/home/hao/Documents/Ground/'
already_apps = []
already_apps_dir = []
os.path.walk(already_dir, already_app_list, None)
print already_apps

dir = '/home/hao/Documents/Loc/'
os.path.walk(dir, visit, None)


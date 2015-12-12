__author__ = 'hao'
import os, re, json#, hashlib

flag = False
#appdir = '/media/hao/Hitachi/BaiduApks/software/504/18/'  # APP_WALLPAPER
#appdir = '/media/hao/Hitachi/Apps/SOCIAL/'  # APP_WALLPAPER
appdir = '/media/hao/Hitachi/BaiduApks/software/502/2/'
outdir = appdir + 'LOC/'

os.system('mkdir ' + outdir)

if flag:
    fn_pattern = re.compile(r'.*(py|log|txt|Controller|json).*')
    list = os.listdir(appdir)  # list files at current dir
    for fline in list:
        if fn_pattern.match(fline):
            continue
        if list.__contains__(fline.split('.apk')[0] + '.json'):
            continue
        #filename = hashlib.md5(fline).hexdigest() 
        #os.system('mv ' + appdir + fline + ' ./' + filename + '.apk')
        os.system('python /media/hao/Hitachi/APKDetails/GetAPKDetails-master/GetApkDetails.py ' + appdir + fline + ' > ' + appdir + fline.split('.apk')[0] + '.json')
        os.system('rm ' + appdir + '*-unpack' + ' -r -f ')
else:
    fline_pattern = re.compile(r'(.*).json')
    no_loc_pattern = re.compile(r'.*(weather|loca).*')
    location_pattern = re.compile(r'.*LOCATION.*')
    list = os.listdir(appdir) # list files at current dir
    counter = 0
    for fline in list:
        if fline_pattern.match(fline):# and not no_loc_pattern.match(fline):
            file = open(appdir + fline)
            try:
                apkjson = json.load(file)
            # print fline

                permission = apkjson[0]["usesPermissionArray"]
            except:
                continue

            if location_pattern.match(str(permission)):
                counter += 1
                apkname = fline.split('.json')[0]
                print apkname
                print permission
                #os.system('cp ' + appdir + apkname + '.html.apk ' + outdir) # if baidu
                os.system('cp ' + appdir + apkname + '.apk ' + outdir)
                os.system('cp ' + appdir + fline + ' ' + outdir)
    print counter
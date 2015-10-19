__author__ = 'hao'
import os, re, json, hashlib

flag = False

appdir = '/media/hao/Hitachi/BaiduApks/software/504/3/'  # APP_WALLPAPER
outdir = appdir + 'non-LOC/'
os.system('mkdir ' + outdir)

if flag:
    fn_pattern = re.compile(r'.*(py|log|txt|Controller).*')
    list = os.listdir(appdir)  # list files at current dir
    for fline in list:
        if fn_pattern.match(fline):
            continue
        filename = hashlib.md5(fline).hexdigest() 
        os.system('mv ' + appdir + fline + ' ./' + filename + '.apk')
        os.system('python /home/watershed2106/Documents/GetAPKDetails-master/GetApkDetails.py ' + appdir + filename + '.apk' + ' > ' + appdir + filename + '.json')
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
            apkjson = json.load(file)
            # print fline
            permission = apkjson[0]["usesPermissionArray"]
            if location_pattern.match(str(permission)):
                continue

            counter += 1
            apkname = fline.split('.json')[0]
            print apkname
            #print permission
            os.system('mv ' + appdir + apkname + '.html.apk ' + outdir + apkname + '.apk')
            os.system('mv ' + appdir + fline + ' ' + outdir)

    print counter
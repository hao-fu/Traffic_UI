# -*- coding: utf-8 -*-

# bag-of-word model of fiest-page UI

import os
import re
import xml.dom.minidom
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import jieba
import sys
import csv
#from sklearn.ensemble import RandomForestClassifier
import mechanize
import cookielib
import urllib
import socket
from bs4 import BeautifulSoup

def get_html(dirname, docid):
    timeout_occurred = True
    br.set_cookiejar(cj)
    # setting
    br.set_handle_equiv(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    base_url = 'http://shouji.baidu.com/soft/item'
    # User-Agent (this is cheating, ok?)
    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0'
    br.addheaders = [('User-agent',
                  'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Chrome/17.0.963.56 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    values = {'docid': docid}
    data = urllib.urlencode(values)
    geturl = base_url + '?' + data
    while timeout_occurred:
        try:
            # Open the page
            br.open(geturl, timeout=1.5)
            html = br.response().read()
            timeout_occurred = False
        except socket.timeout:
                timeout_occurred = True
        except mechanize.URLError as exc:#mechanize.URLError as exc:
            if isinstance(exc.reason, socket.timeout):
                timeout_occurred = True
        # retry
        #br.open(geturl, timeout=5)

    file = open(dirname + '/' + str(docid) + '.html', 'w')
    file.write(html)
    print geturl


def get_descrption(dirname, docid):
    html = dirname + '/' + str(docid) +'.html'
    try:
        soup = BeautifulSoup(open(html, 'r'))
    except:
        get_html(dirname, docid)
    try:
        soup = BeautifulSoup(open(html, 'r'))
        appname_soup = BeautifulSoup(str(soup.select('.app-name')))
        appname = str(appname_soup.select('span')).decode('utf-8')

        descsoup = BeautifulSoup(str(soup.select('.brief-long')))
        desc = str(descsoup.select('p')).decode('utf-8')#.split('data_url')[1]
        wordlist = []
        unseen = []
        str2words(desc, wordlist)
        topic_word_counter = {}
        for word in wordlist:
            if word in unseen:
                #print word
                continue
            else:
                #print word
                unseen.append(word)
                for topic in word_topic.keys():
                    if word in word_topic[topic]:
                        print word
                        if topic not in topic_word_counter.keys():
                            topic_word_counter[topic] = 1
                        else:
                            topic_word_counter[topic] += 1
                        break
        if len(topic_word_counter) == 0:
            return ['topic_LifeStyle', None]
        for topic in sorted(topic_word_counter, key=topic_word_counter.get, reverse=True):
            return [topic, appname]
    except IOError:
        return ['topic_LifeStyle', None]


def str2words(str, wordlist):
    str = re.sub('°', 'DegreeMark', str)
    if is_Chinese_inside(str):
        #print 'Chinese Detected!'
        str = re.sub(u'[^\u4e00-\u9fa5]', '', str)
        words = jieba.cut(str, cut_all=False)
        # words = [w for w in words if not w in stopwords.words("chinese")]
    else:
        #print 'English Detected!'
        str = re.sub('[^a-zA-Z]', ' ', str)  # if English only
        words = str.lower().split()
        #words = [w for w in words if not w in stopwords.words("english")]
        #print words

    # print '/'.join(words) #  do not use print if you want to return
    for word in words:
        wordlist.append(word)
    #return ' '.join(words)
    return words

def DFS_xml(node, nodelist, wordlist):
    if node not in nodelist:
        nodelist.append(node)
        try:
            txt = node.getAttribute('text')
            desc = node.getAttribute('content-desc').lower()
            resid = node.getAttribute('resource-id').lower()
            if txt:
                #print txt
                str2words(txt, wordlist)
                txt = re.sub('(\.|\?|\*)', ' ', txt)
                if re.search(txt, cities) and node.getAttribute('clickable') == 'true':
                    wordlist.append(u'城市Clickable')
                    print 'Found 城市Clickable>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
            elif desc:
                str2words(desc, wordlist)
            elif resid:
                str2words(resid.split('/')[1], wordlist)
            for i in node.childNodes:
                DFS_xml(i, nodelist, wordlist)
        except:
            return

def is_Chinese_inside(content):
    '''
    判断是否是中文需要满足u'[\u4e00-\u9fa5]+'，
    需要注意如果正则表达式的模式中使用unicode，那么
    要匹配的字符串也必须转换为unicode，否则肯定会不匹配。
    '''
    iconvcontent = unicode(content)
    zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
    match = zhPattern.search(iconvcontent)
    res = False
    if match:
        res = True
    return res

def scan_wrapper(dirname, filename, titles, titles_lable, titles_dir, files):
    print dirname + '/' + filename #+ '>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
    dom = xml.dom.minidom.parse(dirname + '/' + filename)
    root = dom.documentElement
    nodelist = []
    wordlist = []
    #wordlist.append(dirname)
    # pkgname as feature
    pkgname = dirname.split('/')
    pkgname = pkgname[len(pkgname) - 1]
    pkgname = str2words(pkgname, wordlist)
    for file in files:
        if re.search('html.apk', file):
            docid = file.split('.html.apk')[0]
            [topic, appname] = get_descrption(dirname, docid)
            if appname != None:
                appname_words = []
                str2words(appname, appname_words)
                for word in appname_words:
                    wordlist.append('a' + word)
            wordlist.append(topic)
            break

    for word in pkgname:
        for dic_word in word_list:
            if re.search(dic_word, word):
                wordlist.append(dic_word)
    DFS_xml(root, nodelist, wordlist)
    titles.append(' '.join(wordlist))
    titles_dir.append(dirname)
    # extract class/lable based on the dir it lies
    if re.search('/0', dirname):
        titles_lable.append(0)
    else:
        titles_lable.append(1)
    print '/'.join(wordlist)
            # titles.append(filename)

def http_exist_visit(files):
    for file in files:
        if re.search('port.*pcap', file):
            return True
    return False

def visit(arg, dirname, files):
    global badcounter

    if re.search('/0/', dirname):
        #badcounter += 1
        if badcounter > 633:
            return

    # if http_flag and not http_exist_visit(files):
    #     if re.search('/0/', dirname):
    #         return

    print dirname + '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
    titles = arg[0]
    titles_lable = arg[1]
    titles_dir = arg[2]
    flag = False
    for f in files:
        if re.search('page.xml', f):
            flag = True
        elif re.search('port.*?csv', f):
            pcapreader = csv.reader(open(dirname + '/' + f, 'rb'), delimiter='\t')
            result = list(pcapreader)
            result = np.array(result)
            try:
                uris = result[:, 26]
                for uri in uris:
                    if uri:
                        #if re.search('map.baidu', uri):
                        if re.search('[^r]ad[^i]', uri) or re.search('stat', uri):
                            if not re.search('weather|map', uri):
                                print uri
            # ignore the parameter part of URI
            #uri = uri.split['?'][0]
                                #os.popen('mv ' + dirname + '/' + f + ' ' + dirname + '/' + f.split('.csv')[0] + '.c1sv')
                        break
            except:
                pass
            # print f
    for filename in files:
        if flag:
            if re.search('page.xml', filename) and not re.search('~', filename):
                if badcounter > 633 and re.search('/0/', dirname):
                        return
                scan_wrapper(dirname, filename, titles, titles_lable, titles_dir, files)
                if re.search('/0/', dirname):
                    badcounter += 1

        else:
            if re.search('hierarchy\.xml', filename) and not re.search('~', filename):
                if badcounter > 633 and re.search('/0/', dirname):
                        return
                scan_wrapper(dirname, filename, titles, titles_lable, titles_dir, files)
                #if re.search('/0/', dirname):
                 #   break
                if re.search('/0/', dirname):
                    badcounter += 1




def get_data(dir):
    titles = []
    titles_lable = []
    titles_dir = []
    os.path.walk(dir, visit, [titles, titles_lable, titles_dir])

    if len(titles) != len(titles_lable) or len(titles_dir) != len(titles):
        print 'ERROR'
        exit(1)
    # Initialize the "CountVectorizer" object, which is scikit-learn's bag of words tool.
    vectorizer = CountVectorizer(analyzer = "word",   \
                             tokenizer = None,    \
                             preprocessor = None, \
                             stop_words = None,   \
                             max_features = 5000)
    # fit_transform() does two functions: First, it fits the model
    # and learns the vocabulary; second, it transforms our training data
    # into feature vectors. The input to fit_transform should be a list of
    # strings.
    titles_vocab_mat = vectorizer.fit_transform(titles)
    # Numpy arrays are easy to work with, so convert the result to an array
    #print vectorizer.vocabulary_  # a dict, the value is the index
    train_data_features = titles_vocab_mat.toarray()
    print train_data_features.shape
    # Take a look at the words in the vocabulary
    vocab = vectorizer.get_feature_names()
    print '/'.join(vocab)
    # Sum up the counts of each vocabulary word
    dist = np.sum(train_data_features, axis=0)
    total_words = 0
    for i in train_data_features:
        #print sum(i)
        total_words += sum(i)
    print total_words

    arffname = 'front_page'
    # save to arff
    #print '@RELATION ' + arffname
    train_file.write('@RELATION ' + arffname + '\n')
    # For each, print the vocabulary word and the number of times it appears in the training set
    train_file.write('@ATTRIBUTE dirname STRING\n')
    if numeric_flag:
        for tag, count in zip(vocab, dist):
            #print '@ATTRIBUTE word_freq_' + tag + ' NUMERIC'
            train_file.write('@ATTRIBUTE word_freq_' + tag.encode('utf-8') + ' NUMERIC\n')
    else:
        for tag, count in zip(vocab, dist):
            #print '@ATTRIBUTE word_freq_' + tag + ' NUMERIC'
            train_file.write('@ATTRIBUTE word_freq_' + tag.encode('utf-8') + ' {0, 1}\n')
            #print count
    train_file.write('@ATTRIBUTE class {0, 1}\n')
    #print '\n@DATA'
    train_file.write('\n@DATA\n')


    counter = 0
    for title_counts in train_data_features:
        train_file.write(titles_dir[counter] + ',')
        # print title_counts
        #word_freq_list = []
        for word_count in title_counts:
            # calculate freq of words = percentage of words in front page that match WORD
            # i.e. 100 * (number of times the WORD appears in the front_page) /  total number of words in front page

            #word_freq_list.append(word_freq)
            #sys.stdout.write(str(word_freq) + ',')
            if numeric_flag:
                word_freq = 100 * float(word_count) / float(total_words)
                train_file.write(str(word_freq) + ',')
            else:
                if int(word_count) > 0:
                    train_file.write('1,')
                else:
                    train_file.write('0,')
        #sys.stdout.write(str(titles_lable[counter]) + '\n')
        train_file.write(str(titles_lable[counter]) + '\n')
        counter += 1


    # write instance-dir map file
    for title in titles_dir:
        ui_dir_file.write(title + '\n')

br = mechanize.Browser()
cj = cookielib.LWPCookieJar()

jieba.load_userdict("user.dict")
city_list = [u'北京市',u'海淀区',u'东城区',u'西城区',u'宣武区',u'丰台区',u'朝阳区',u'崇文区',u'大兴区',u'石景山区',u'门头沟区',u'房山区',u'通州区',u'顺义区',u'怀柔区',u'昌平区',u'平谷区',u'密云县',u'延庆县',u'天津市',u'和平区',u'河西区',u'河北区',u'河东区',u'南开区',u'红桥区',u'北辰区',u'津南区',u'武清区',u'塘沽区',u'西青区',u'汉沽区',u'大港区',u'宝坻区',u'东丽区',u'蓟县',u'静海县',u'宁河县',u'上海',u'黄浦区',u'卢湾区',u'徐汇区',u'长宁区',u'静安区',u'普陀区',u'闸北区',u'杨浦区',u'虹口区',u'闵行区',u'宝山区',u'嘉定区',u'浦东新区',u'金山区',u'松江区',u'青浦区',u'南汇区',u'奉贤区',u'崇明县',u'重庆',u'渝中区',u'大渡口区',u'江北区',u'沙坪坝区',u'九龙坡区',u'南岸区',u'北碚区',u'万盛区',u'双桥区',u'渝北区',u'巴南区',u'万州区',u'涪陵区',u'黔江区',u'长寿区',u'江津区',u'永川区',u'南川区',u'綦江县',u'潼南县',u'铜梁县',u'大足县',u'荣昌县',u'璧山县',u'垫江县',u'武隆县',u'丰都县',u'城口县',u'梁平县',u'开县',u'巫溪县',u'巫山县',u'奉节县',u'云阳县',u'忠县',u'石柱土家族自治县',u'彭水苗族土家族自治县',u'酉阳苗族自治县',u'秀山土家族苗族自治县',u'新疆维吾尔',u'乌鲁木齐',u'克拉玛依县级市',u'石河子',u'阿拉尔市',u'图木舒克',u'五家渠',u'哈密',u'吐鲁番',u'阿克苏',u'喀什',u'和田',u'伊宁',u'塔城',u'阿勒泰',u'奎屯',u'博乐',u'昌吉',u'阜康',u'库尔勒',u'阿图什',u'乌苏',u'西藏',u'拉萨',u'县级市',u'日喀则',u'宁夏回族',u'银川',u'石嘴山',u'吴忠',u'固原',u'中卫',u'县级市',u'青铜峡市',u'灵武市',u'内蒙古',u'呼和浩特',u'包头',u'乌海',u'赤峰',u'通辽',u'鄂尔多斯',u'呼伦贝尔',u'巴彦淖尔',u'乌兰察布',u'县级市',u'霍林郭勒市',u'满洲里市',u'牙克石市',u'扎兰屯市',u'根河市',u'额尔古纳市',u'丰镇市',u'锡林浩特市',u'二连浩特市',u'乌兰浩特市',u'阿尔山市',u'广西壮族',u'南宁',u'柳州',u'桂林',u'梧州',u'北海',u'崇左',u'来宾',u'贺州',u'玉林',u'百色',u'河池',u'钦州',u'防城港',u'贵港',u'县级市',u'岑溪',u'凭祥',u'合山',u'北流',u'宜州',u'东兴',u'桂平',u'省级行政单位',u'黑龙江',u'哈尔滨',u'大庆',u'齐齐哈尔',u'佳木斯',u'鸡西',u'鹤岗',u'双鸭山',u'牡丹江',u'伊春',u'七台河',u'黑河',u'绥化',u'县级市',u'五常',u'双城',u'尚志',u'纳河',u'虎林',u'密山',u'铁力',u'同江',u'富锦',u'绥芬河',u'海林',u'宁安',u'穆林',u'北安',u'五大连池',u'肇东',u'海伦',u'安达',u'吉林',u'长春',u'吉林',u'四平',u'辽源',u'通化',u'白山',u'松原',u'白城',u'县级市',u'九台市',u'榆树市',u'德惠市',u'舒兰市',u'桦甸市',u'蛟河市',u'磐石市',u'公主岭市',u'双辽市',u'梅河口市',u'集安市',u'临江市',u'大安市',
          u'洮南市',u'延吉市',u'图们市',u'敦化市',u'龙井市',u'珲春市',u'和龙市',u'辽宁',u'沈阳',u'大连',u'鞍山',u'抚顺',u'本溪',u'丹东',u'锦州',u'营口',u'阜新',u'辽阳',u'盘锦',u'铁岭',u'朝阳',u'葫芦岛',u'县级市',u'新民',u'瓦房店',u'普兰',u'庄河',u'海城',u'东港',u'凤城',u'凌海',u'北镇',u'大石桥',u'盖州',u'灯塔',u'调兵山',u'开原',u'凌源',u'北票',u'兴城',u'河北',u'石家庄',u'唐山',u'邯郸',u'秦皇岛',u'保定',u'张家口',u'承德',u'廊坊',u'沧州',u'衡水',u'邢台',u'县级市',u'辛集市',u'藁城市',u'晋州市',u'新乐市',u'鹿泉市',u'遵化市',u'迁安市',u'武安市',u'南宫市',u'沙河市',u'涿州市',u'定州市',u'安国市',u'高碑店市',u'泊头市',u'任丘市',u'黄骅市',u'河间市',u'霸州市',u'三河市',u'冀州市',u'深州市',u'山东',u'济南',u'青岛',u'淄博',u'枣庄',u'东营',u'烟台',u'潍坊',u'济宁',u'泰安',u'威海',u'日照',u'莱芜',u'临',u'沂',u'德州',u'聊城',u'菏泽',u'滨州',u'县级市',u'章丘',u'胶南',u'胶州',u'平度',u'莱西',u'即墨',u'滕州',u'龙口',u'莱阳',u'莱州',u'招远',u'蓬莱',u'栖霞',u'海阳',u'青州',u'诸城',u'安丘',u'高密',u'昌邑',u'兖州',u'曲阜',u'邹城',u'乳山',u'文登',u'荣成',u'乐陵',u'临清',u'禹城',u'江苏',u'南京',u'镇江',u'常州',u'无锡',u'苏州',u'徐州',u'连云港',u'淮安',u'盐城',u'扬州',u'泰州',u'南通',u'宿迁',u'县级市',u'江阴市',u'宜兴市',u'邳州市',u'新沂市',u'金坛市',u'溧阳市',u'常熟市',u'张家港市',u'太仓市',u'昆山市',u'吴江市',u'如皋市',u'通州市',u'海门市',u'启东市',u'东台市',u'大丰市',u'高邮市',u'江都市',u'仪征市',u'丹阳市',u'扬中市',u'句容市',u'泰兴市',u'姜堰市',u'靖江市',u'兴化市',u'安徽',u'合肥',u'蚌埠',u'芜湖',u'淮南',u'亳州',u'阜阳',u'淮北',u'宿州',u'滁州',u'安庆',u'巢湖',u'马鞍山',u'宣城',u'黄山',u'池州',u'铜陵',u'县级市',u'界首',u'天长',u'明光',u'桐城',u'宁国',u'浙江',u'杭州',u'嘉兴',u'湖州',u'宁波',u'金华',u'温州',u'丽水',u'绍兴',u'衢州',u'舟山',u'台州',u'县级市',u'建德市',u'富阳市',u'临安市',u'余姚市',u'慈溪市',u'奉化市',u'瑞安市',u'乐清市',u'海宁市',u'平湖市',u'桐乡市',u'诸暨市',u'上虞市',u'嵊州市',u'兰溪市',u'义乌市',u'东阳市',u'永康市',u'江山市',u'临海市',u'温岭市',u'龙泉市',u'福建',u'福州',u'厦门',u'泉州',u'三明',u'南平',u'漳州',u'莆田',u'宁德',u'龙岩',u'县级市',u'福清市',u'长乐市',u'永安市',u'石狮市',u'晋江市',u'南安市',u'龙海市',u'邵武市',u'武夷山',u'建瓯市',u'建阳市',u'漳平市',u'福安市',u'福鼎市',u'广东',u'广州',u'深圳',u'汕头',u'惠州',u'珠海',u'揭阳',u'佛山',u'河源',u'阳江',u'茂名',u'湛江',u'梅州',u'肇庆',u'韶关',u'潮州',u'东莞',u'中山',
          u'清远',u'江门',u'汕尾',u'云浮',u'县级市',u'增城市',u'从化市',u'乐昌市',u'南雄市',u'台山市',u'开平市',u'鹤山市',u'恩平市',u'廉江市',u'雷州市 吴川市',u'高州市',u'化州市',u'高要市',u'四会市',u'兴宁市',u'陆丰市',u'阳春市',u'英德市',u'连州市',u'普宁市',u'罗定市',u'海南',u'海口',u'三亚',u'县级市',u'琼海',u'文昌',u'万宁',u'五指山',u'儋州',u'东方',u'云南',u'昆明',u'曲靖',u'玉溪',u'保山',u'昭通',u'丽江',u'普洱',u'临沧',u'县级市',u'安宁市',u'宣威市',u'个旧市',u'开远市',u'景洪市',u'楚雄市',u'大理市',u'潞西市',u'瑞丽市',u'贵州',u'贵阳',u'六盘水',u'遵义',u'安顺',u'县级市',u'清镇市',u'赤水市',u'仁怀市',u'铜仁市',u'毕节市',u'兴义市',u'凯里市',u'都匀市',u'福泉市',u'四川',u'成都',u'绵阳',u'德阳',u'广元',u'自贡',u'攀枝花',u'乐山',u'南充',u'内江',u'遂宁',u'广安',u'泸州',u'达州',u'眉山',u'宜宾',u'雅安',u'资阳',u'县级市',u'都江堰市',u'彭州市',u'邛崃市',u'崇州市',u'广汉市',u'什邡市',u'绵竹市',u'江油市',u'峨眉山市',u'阆中市',u'华蓥市',u'万源市',u'简阳市',u'西昌市',u'湖南',u'长沙',u'株洲',u'湘潭',u'衡阳',u'岳阳',u'郴州',u'永州',u'邵阳',u'怀化',u'常德',u'益阳',u'张家界',u'娄底',u'县级市',u'浏阳市',u'醴陵市',u'湘乡市',u'韶山市',u'耒阳市',u'常宁市',u'武冈市',u'临湘市',u'汨罗市',u'津市市',u'沅江市',u'资兴市',u'洪江市',u'冷水江市',u'涟源市',u'吉首市',u'湖北',u'武汉',u'襄樊',u'宜昌',u'黄石',u'鄂州',u'随州',u'荆州',u'荆门',u'十堰',u'孝感',u'黄冈',u'咸宁',u'县级市',u'大冶市',u'丹江口市',u'洪湖市',u'石首市',u'松滋市',u'宜都市',u'当阳市',u'枝江市',u'老河口市',u'枣阳市',u'宜城市',u'钟祥市',u'应城市',u'安陆市',u'汉川市',u'麻城市',u'武穴市',u'赤壁市',u'广水市',u'仙桃市',u'天门市',u'潜江市',u'恩施市',u'利川市',u'河南',u'郑州',u'洛阳',u'开封',u'漯河',u'安阳',u'新乡',u'周口',u'三门峡',u'焦作',u'平顶山',u'信阳',u'南阳',u'鹤壁',u'濮阳',u'许昌',u'商丘',u'驻马店',u'县级市',u'巩义市',u'新郑市',u'新密市',u'登封市',u'荥阳市',u'偃师市',u'汝州市',u'舞钢市',u'林州市',u'卫辉市',u'辉县市',u'沁阳市',u'孟州市',u'禹州市',u'长葛市',u'义马市',u'灵宝市',u'邓州市',u'永城市',u'项城市',u'济源市',u'山西',u'太原',u'大同',u'忻州',u'阳泉',u'长治',u'晋城',u'朔州',u'晋中',u'运城',u'临汾',u'吕梁',u'县级市',u'古交',u'潞城',u'高平',u'介休',u'永济',u'河津',u'原平',u'侯马',u'霍州',u'孝义',u'汾阳',u'陕西',u'西安',u'咸阳',u'铜川',u'延安',u'宝鸡',u'渭南',u'汉中',u'安康',u'商洛',u'榆林',u'县级市',u'兴平市',u'韩城市',u'华阴市',u'甘肃',u'兰州',u'天水',u'平凉',u'酒泉',u'嘉峪关',
          u'金昌',u'白银',u'武威',u'张掖',u'庆阳',u'定西',u'陇南',u'玉门市',u'敦煌市',u'临夏市',u'合作市',u'青海',u'西宁',u'县级市',u'格尔木',u'德令哈',u'江西',u'南昌',u'九江',u'赣州',u'吉安',u'鹰潭',u'上饶',u'萍乡',u'景德镇',u'新余',u'宜春',u'抚州',u'县级市',u'乐平市',u'瑞昌市',u'贵溪市',u'瑞金市',u'南康市',u'井冈山市',u'丰城市',u'樟树市',u'高安市',u'德兴市',u'台湾',u'市',u'台北',u'台中',u'基隆',u'高雄',u'台南',u'新竹',u'嘉义',u'县级市',u'板桥市',u'宜兰市',u'竹北市',u'桃园市',u'苗栗市',u'丰原市',u'彰化市',u'南投市',u'太保市',u'斗六市',u'新营市',u'凤山市',u'屏东市',u'台东市',u'花莲市',u'马公市',u'特别行政区',u'香港',u'中西区',u'东区',u'九龙城区',u'观塘区',u'南区',u'深水埗区',u'黄大仙区',u'湾仔区',u'油尖旺区',u'离岛区',u'葵青区',u'北区',u'西贡区',u'沙田区',u'屯门区',u'大埔区',u'荃湾区',u'元朗区',u'离岛',u'氹仔',u'路环']
cities = ' '.join(city_list)
word_list = ['tech', 'weather', 'ad', 'forecast', 'lauch', 'bus', 'navi', 'map', 'trip', 'city', 'home']
word_topic = {'topic_health': [u'健身', u'运动', u'健康', u'体重', u'身体', u'锻炼'],
              'topic_sports': [u'足球', u'队员', u'篮球', u'跑步'],
              'topic_weather':[u'天气', u'预报', u'温度', u'湿度', 'PM2\.5'],
              'topic_map': [u'旅行', u'地图', u'地理', u'GPS', u'导航', u'旅游']} # combine health and sport
numeric_flag = False
badcounter = 0
#print cities
#nltk.download() # download text data sets, including stop words
#train_dir = '/home/watershed2106/Documents/LOC/samplesLoc/'
http_flag = True
if http_flag:
    train_file = open('train_UI.arff', 'w')
else:
    train_file = open('train_UI.arff', 'w')
ui_dir_file = open('ui_instance_map.txt', 'w')
train_dir = '/home/hao/Documents/Ground/'
#train_dir = '/home/hao/Documents/Untitled/'
get_data(train_dir)
train_file.close()
ui_dir_file.close()
print 'num of bad apps: ' + str(badcounter)


#print "Training the random forest..."
# Initialize a Random Forest classifier with 100 trees
#forest = RandomForestClassifier(n_estimators=100)

# Fit the forest to the training set, using the bag of words as
# features and the sentiment labels as the response variable
#
# This may take a few minutes to run
#forest = forest.fit(train_data_features, train["sentiment"] )
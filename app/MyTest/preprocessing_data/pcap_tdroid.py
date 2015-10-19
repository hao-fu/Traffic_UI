__author__ = 'hao'

from scapy.layers.inet import IP, TCP
from scapy.all import *

# match flow in pcap to the flow reported by taintdroid

def filter_pcap(dirname, pcap, time, port, ip):
    try:
        rdpcap(dirname + '/' + ip + '_' + time + '_filtered_port_num_' + str(port) + '.pcap')
        return
    except:
        pass
    try:
        pkts = rdpcap(dirname + '/' + pcap)
    except IOError as e:
        print e.args
        return
    filtered = (pkt for pkt in pkts if
                TCP in pkt
                and (pkt[TCP].sport == port or pkt[TCP].dport == port)
                and (pkt[IP].dst == ip or pkt[IP].src == ip))
    wrpcap(dirname + '/' + ip + '_' + time + '_filtered_port_num_' + str(port) + '.pcap', filtered)
    # for pkt in pkts:
    #     if TCP in pkt:
    #         if pkt[TCP].sport == port or pkt[TCP].dport == port:
    #             print 'Found'

    #print 'done'


def write_pcap_txt(dirname, pcap):
    result = os.popen('parse_pcap ' + dirname + '/' + pcap + ' > ' + dirname + '/' + pcap.split('.pcap')[0] + '.txt')
    print result

def match_flow(pcap_txt, ip, data, time, dirname, pcap):
    data = data.replace('?', '\?')
    data = data.replace('(', '\(')
    data = data.replace(')', '\)')
    data = data.replace('[', '\[')
    try:
        pcap_txt = open(pcap_txt, 'r')
    except IOError:
        #print dirname + '/' + pcap
        write_pcap_txt(dirname, pcap)
        pcap_txt = open(pcap_txt, 'r')
        #return False
    lines = pcap_txt.readlines()
    flag = False
    # examine all lines in pcap-txt, check whether match
    for i in range(len(lines)):
        #print line
        #try:
        line = lines[i]
        if re.search(data, line):
            flag = True
            if ip not in iptable:
                iptable.append(ip)
            try:
                domain = line.split('//')[1].split('/')[0]
                if domain not in domain_list:
                    domain_list.append(domain)
                    if not str(ip) in ip_domain:
                        ip_domain[str(ip)] = [domain]
                    else:
                        ip_domain[str(ip)].append(domain)
                if re.search('http', data):
                    uri = data
                else:
                    try:
                        uri = domain + '/' + data.split('\\')[1]
                    except:
                        uri = domain + data
                if uri not in uri_list:
                    uri_list.append(uri)
            except IndexError:
                print 'Data: ' + data
                print 'ERROR URI: ' + line
                continue
            try:
                # extract port number from pcap_txt
                port = int(lines[i - 1].split(':')[1].split(']')[0])
            except:
                continue
            #print port
            filter_pcap(dirname, pcap, time, port, ip)
    if not flag:
        print data
        return False
    else:
        return True


def visit(arg, dirname, files):
    global counter
    for filename in files:
        if re.search(r'.*?-.*?-.*?log', filename):
            #print dirname + '/' + filename
            file = open(dirname + '/' + filename, 'r') # open taintdroid report
            lines = file.readlines()
            flag = False
            for line in lines:
                # if find location related taint
                if re.search('Location', line) and not re.search('SSL', line):
                    pcap = dirname.split('/')
                    if re.search('apk', filename):
                        time = filename.split('apk')[1].split('.')[0]
                    else:
                        if re.search('070', filename):
                            time = '070' + filename.split('070')[1].split('.')[0]
                        elif re.search('06', filename):
                            #time = '06' + filename.split('06')[1].split('.')[0]
                            time = ''
                    pcap = pcap[len(pcap) - 1] + time + '.pcap'
                    #write_pcap_txt(dirname, pcap)
                    line = line.split(', ')
                    ip = line[1]
                    # extract http header/payload info from taintdroind report
                    try:
                        # if get/post inside
                        data = line[len(line) - 2].split(' HTTP')[0].split(' ')[1]
                    except:
                        data = line[len(line) - 2].split(' HTTP')[0]
                    if not data:
                        for l in line:
                            if re.search('POST', l):
                                data = l.split(' HTTP')[0].split(' ')[1]
                                break
                            elif re.search('GET', l):
                                data = l.split(' HTTP')[0].split(' ')[1]
                                break

                    #print data
                    # match flow in pcap txt report
                    result = match_flow(dirname + '/' + pcap.split('.pcap')[0] + '.txt', ip, data, time, dirname, pcap)
                    if not result:
                        if not flag:
                            counter += 1
                            flag = True

counter = 0
iptable = []
domain_list = []
uri_list = []
#dir = '/home/hao/Documents/Ground/1/edu'
dir = '/home/hao/Documents/Loc/social'
ip_domain = {}
os.path.walk(dir, visit, None)
print 'Missed: ' + str(counter)

print iptable
print len(iptable)

print domain_list
print len(domain_list)

print ip_domain
print uri_list
print len(uri_list)

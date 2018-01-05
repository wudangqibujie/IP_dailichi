import urllib.request
from lxml import etree
import time

def get_url(url):
    url_list = []
    for i in range(11,31):
        url_new = url + str(i)
        url_list.append(url_new)
    return url_list

def get_content(url):
    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36"
    headers = {"User-Agent":user_agent}
    req = urllib.request.Request(url = url,headers=headers)
    res = urllib.request.urlopen(req)
    content = res.read()
    return content.decode("utf-8")

def get_info(content):
    datas_ip = etree.HTML(content).xpath('//table[contains(@id,"ip_list")]/tr/td[2]/text()')
    datas_port = etree.HTML(content).xpath('//table[contains(@id,"ip_list")]/tr/td[3]/text()')
    datas_category = etree.HTML(content).xpath('//table[contains(@id,"ip_list")]/tr/td[6]/text()')
    with open("data.txt",'w') as fd:
        for i in range(0,len(datas_ip)):
            out = u""
            out += u"" + datas_ip[i]
            out += u":" + datas_port[i]
            out += u":" + datas_category[i]
            fd.write(out+u"\n")

def verif_ip(ip,port):
    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36"
    headers = {'User-Agent':user_agent}
    proxy = {'http':'http://%s:%s'%(ip,port)}
    print(proxy)

    proxy_handler = urllib.request.ProxyHandler(proxy)
    opener = urllib.request.build_opener(proxy_handler)
    urllib.request.install_opener(opener)
    test_url = "https://www.baidu.com/"
    req = urllib.request.Request(url=test_url,headers=headers)
    time.sleep(6)
    try:
        res = urllib.request.urlopen(req)
        time.sleep(3)
        content = res.read()
        if content:
            print("that is OK")
            with open("data2.txt","a") as fd:
                fd.write(ip+u":" + port)
                fd.write("\n")
        else:
            print("-------------its not ok-------------")
    except urllib.request.URLError as e:
        print(e.reason)

if __name__ == "__main__":
    url = "http://www.xicidaili.com/nn/"
    url_list = get_url(url)
    for i in url_list:
        print(i)
        conntent = get_content(i)
        time.sleep(3)
        get_info(conntent)
    with open("data.txt","r") as fd:
        datas = fd.readlines()
        for data in datas:
            print(data.split(u":")[0],data.split(u":")[1],data.split(u":")[2])
            verif_ip(data.split(u":")[0],data.split(u":")[1])





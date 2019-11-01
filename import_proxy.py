import urllib
import time
import re
from lxml import etree
import MySQLdb

database = {
    'host': '172.200.9.5',
    'user': 'root',
    'passwd': '123qwe',
    'db': 'acdb'
}
class DataBaseUtil(object):
    def __init__(self):
        self.host = database['host']
        self.user = database['user']
        self.passwd = database['passwd']
        self.db = database['db']


    @classmethod
    def getConn(cls):
        conn = None
        is_false = True
        while is_false:
            try:
                conn = MySQLdb.connect(db=database['db'],host=database['host'],user=database['user'],passwd=database['passwd'],charset='utf8')
                is_false = False
            except:
                time.sleep(0.5)
        return conn

    @classmethod
    def select(cls,sql):
        conn = cls.getConn()
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        conn.commit()
        conn.close()
        return result

def get(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

while False:
    url = 'http://ip.zdaye.com/'
    content = get(url)
    content = content.decode('gbk')
    dom = etree.HTML(content)
    table = dom.xpath("descendant::table[@id='ipc']")[0]
    trs = table.xpath("descendant::tr")
    base_zero = 0
    i = -1
    for tr in trs:
        i +=1
        if i==0:
            continue
        if i==1:
            zero = tr.xpath("td")[1].xpath('@v')[0].split('#')[0]
            base_zero = int(zero)
        ip = tr.xpath("td")[0].text
        ip_v_list = tr.xpath("td")[0].xpath('@v')[0].split('#')
        num = ''
        for it in ip_v_list:
            t_n = int(it) - base_zero
            num = str(t_n) + num
        ip = ip[0:ip.index('w')] + num
        print ip
        # DataBaseUtil.execute("replace into train_proxy(ip,port,is_use) value('%s','%s',0)" %(ip,port))
        # print ip,port
    time.sleep(100)
def deal(s):
    c = r'[0-9]+'
    a = re.compile(c)
    r = re.findall(a,s)
    return r[0]
base_search = "select count(*) from basepoi where id = %s"

ids_file = open('ids.txt','r')
result = open("result.csv",'w')
for line in ids_file.readlines():
    id = deal(line)
    count = DataBaseUtil.select(base_search % id)[0]
    exist = 1
    if count == 0:
        exist = 0
    result.write('%s,%s\n' % (id,exist))














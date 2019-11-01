# -*- coding: utf-8 -*-
# 日志的类型
# CATEGORY_LOG = 'dp-shop'
CATEGORY_LOG = 'station-12306'
#抓取间隔
FREQUENCY_TIME = 5

#是否需要增加日期
DATE_NEED_ADD = False

#是否使用代理
IF_USE_PROXY = False 

#代理使用
PROXY_FREQUENCY_TIME = 10

#通信状态
OK_CODE         = 200
REDIRECT_CODE   = 302
NO_CONTENT      = 204
NOT_FOUND       = 404

STATUS_OK           = 1
STATUS_ERROR        = 2
STATUS_NOT_FOUND    = 3

# nice 最大值设置
CATCH_NUM = 20

DOWNLOAD_WORKERS_SIZE = 1
EXTRACTOR_WORKERS_SIZE =4
PROXY_CHECKER_SIZE = 0 
LINKS_QUEUE_MIN_SIZE = 12288

BATCH_ADD_LINKS_SIZE = 4096

#代理检测链接
check_url = "http://www.ly.com/huochepiao/Handlers/TrainListSearch.ashx?to=baigou&from=tielingxi&trainDate=2017-04-22&PlatId=1&callback=jQuery183004485401697308511"

# check_url = "http://mapi.dianping.com/searchshop.json?start=0&regionid=0&categoryid=10&cityid=2&locatecityid=2&maptype=0"
# check_url = "http://catfront.dianping.com/api/batch?v=1&sdk=1.4.31"

# check_heades  = [
#     "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#     "Accept-Language:zh-CN,zh;q=0.8,en;q=0.6"
#     "Connection: close",
#     "Host: www.dianping.com",
#     "User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
#     "Upgrade-Insecure-Requests:1"]
check_heades = [
    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Charset: utf-8, gbk*,*",
    "Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3"
    "Connection: close",
    "Host: www.ly.com",
    "Via: WTP/1.1 HBWH-PS-WAP-GW11.hbwh.monternet.com (Nokia WAP Gateway 4.0/CD3/4.1.79)",
    "X-Forwarded-For: 127.0.0.1",
]

database = {
    'host': '172.16.19.203',
    'user': 'data',
    'passwd': 'opensesame',
    'db': 'img_upload'
}

# database = {
#     'host': '127.0.0.1',
#     'user': 'root',
#     'passwd': '',
#     'db': 'train'
# }
# database = {
#     'host': '192.100.2.31',
#     'user': 'data',
#     'passwd': 'opensesame',
#     'db': 'traincrawler'
# }

#DOWNLOAD_HEADERS = [
#    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Charset: utf-8, gbk*,*",
#    "Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3"
#    "Connection: close",
#    "Host: www.ly.com",
#    "Via: WTP/1.1 HBWH-PS-WAP-GW11.hbwh.monternet.com (Nokia WAP Gateway 4.0/CD3/4.1.79)",
#    "X-Forwarded-For: 127.0.0.1",
#]

DOWNLOAD_HEADERS = [
     "Accept:*/*",
     "Accept-Encoding:gzip, deflate, sdch", 
     "Accept-Language:zh-CN,zh;q=0.8,en;q=0.6"
     "Connection:keep-alive",
     "Referer:https://kyfw.12306.cn/otn/leftTicket/init",
     "X-Requested-With:XMLHttpRequest",
     "Host: kyfw.12306.cn"
]


# DOWNLOAD_HEADERS = [
#     "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#     "Accept-Language:zh-CN,zh;q=0.8,en;q=0.6"
#     "Connection: close",
#     "Host: www.dianping.com",
#     "Upgrade-Insecure-Requests:1",
#     "Cookie:_hc.v=\"\"8e472d46-41cf-4dbc-9267-63ffa3b49e8d.1495254300\"\"; PHOENIX_ID=0a010444-15c2419f777-f1114c8; JSESSIONID=3C6AC9006AD26231205475F2C61FA8FA; aburl=1; cy=2; cye=beijing; __mta=46464664.1495254306523.1495254306523.1495254306523.1"
# ]


PC_USER_AGENTS = [
#"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9a3pre) Gecko/20070330",
#"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2) Gecko/20100115 Ubuntu/10.04 (lucid) Firefox/3.6",
"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (.NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022; .NET CLR 1.1.4322; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)",
"Mozilla/5.0 (Windows; U; Windows NT 6.0; de; rv:1.9.0.15) Gecko/2009101601 Firefox 2.1 (.NET CLR 3.5.30729)",
"Mozilla/5.0 (compatible; N; Windows NT 5.1; en;) Gecko/20080325 Firefox/2.0.0.13",
#"Opera/9.99 (Windows NT 5.1; U; pl) Presto/9.9.9",
#"Opera/9.24 (Macintosh; PPC Mac OS X; U; en)",
"Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.0) Gecko/20060728 Firefox/1.5.0 Opera 9.24",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.24",
#"Mozilla/4.0 (compatible; MSIE 6.0; Mac_PowerPC; en) Opera 9.24",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows 98; en) Opera 8.0",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; MyIE2; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0)",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; MyIE2; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
#"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; GTB6.4; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; MSSDMC2.5.2219.1)",
"Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; .NET CLR 1.0.3705; Media Center PC 3.1; Alexa Toolbar; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
#"Mozilla/5.0 (MSIE 7.0; Macintosh; U; SunOS; X11; gu; SV1; InfoPath.2; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648)",
#"Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 6.0; WOW64; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; c .NET CLR 3.0.04506; .NET CLR 3.5.30707; InfoPath.1; el-GR)",
#"Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; MAXTHON 2.0)",
"Mozilla/4.0 (compatible; MSIE 7.9; Windows NT 6.0; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506; InfoPath.2; MAXTHON 2.0)",
"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.2 (KHTML, like Gecko) Chrome/6.0",
"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.4 (KHTML, like Gecko) Chrome/5.0.370.0 Safari/533.4",
"Mozilla/5.0 (Windows; U; Windows NT 5.1; de-DE) Chrome/4.0.223.3 Safari/532.2",
#"Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.2 (KHTML, like Gecko) Chrome/4.0.223.2 Safari/532.2",
"Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en; rv:1.8.1.4pre) Gecko/20070521 Camino/1.6a1pre",
"Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; it; rv:1.8.1.21) Gecko/20090327 Camino/1.6.7 (MultiLang) (like Firefox/2.0.0.21pre)",
"Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en; rv:1.8.1.6) Gecko/20070809 Firefox/2.0.0.6 Camino/1.5.1",
"Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en; rv:1.8.1.6) Gecko/20070809 Camino/1.5.1"]

PC_USER_AGENTS_SUM = len(PC_USER_AGENTS)

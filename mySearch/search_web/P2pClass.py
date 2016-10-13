#! /usr/bin/env python
# -*- coding: utf-8 -*-
import csv, time
import requests
from bs4 import BeautifulSoup
import random
import os
from string import Template
import threading
from xmlsetting import getValue

class P2P(object):
    def __init__(self):
        self.rootpath = '/home/chenkun/p2pdata/'
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'}
        self.proxies = {'http': 'http://182.90.252.10:2226'}
        self.count_req = 0
        self.count_suc = 0
        self.delay = float(getValue('spiderDelay'))  # 每页爬取的时间延迟
        self.timeout=float(getValue('timeout'))
        self.maxrequestnums=30
        # self.bidList=[]

    def repchar(self, strtext):
        return unicode(strtext).replace(' ', '').replace(',', ' ').replace('\n', ' ').replace('\r', ' ') \
            .replace('  ', '').strip().encode('utf-8')

    def gethtml(self, url=None, headers=None, proxies=None,timeout=60):
        try:
            r = requests.get(url,proxies=proxies,headers=headers,timeout=timeout)
        except:
            print url, ': bad'
            return None
        return r._content

    def getagent(self):
        ipfile = open(self.rootpath + 'ipagent/ipagent.csv', 'r')
        iplist = []
        for each in csv.reader(ipfile):
            iplist.append(each)
        ipfile.close()
        return iplist

    def pagelist(self, soup, bidList, platform):
        pass

    def writetoDB_list(self):
        # list信息
        coninfo = "psql -h 127.0.0.1 -p 5432 -U kun -d p2p"
        csvpath = self.rootpath + 'wdlist/db_bidlist.csv'
        os_ex1 = '''cat $path | $count -c "copy $table (title,platform,url,sum,
        limittime,rate,process,peoplenum,heatvalue,decription,indexsum,indextime,indexrate)
        from stdin delimiter ',';" ;'''
        os_ex1 = Template(os_ex1)
        os.system(os_ex1.substitute(path=csvpath, count=coninfo, table='list_source'))

    def writetoDB_monitor(self):
        # 监控信息
        coninfo = "psql -h 127.0.0.1 -p 5432 -U kun -d p2p"
        csvpath = self.rootpath + 'wdlist/db_monitor.csv'
        os_ex2 = '''cat $path | $count -c "copy $table (platform,count_req,count_suc)
        from stdin delimiter ',';";'''
        os_ex2 = Template(os_ex2)
        os.system(os_ex2.substitute(path=csvpath, count=coninfo, table='sp_reqinfo'))

    def clandtocsv(self, pagenums=50, tlock=None, mlock=None,elock=None):
        bidlist,iserror = self.spider(pagenums)
        platform=''
        csvlist = []
        c = 0
        for bid in bidlist:
            c += 1
            if c > 100000:
                break
            title = bid[0]
            url = bid[1]
            summoney = bid[3]
            # print 'bid[4]:',bid[4]
            limitTime = bid[4].replace('个月', '')
            rate = bid[2].replace('%', '')
            if '~' in rate:
                rate = rate[:rate.index('~')]
            process = bid[6].replace('%', '')
            peoplenum = bid[5]

            if peoplenum == '':
                peoplenum = -1
            #

            if limitTime.lower() == 'null':
                limitTime = '1'

            heatValue = random.randint(30, 100)
            platform = bid[7]
            description = bid[8]

            if description == '':
                description = ''.join(['来自', platform, '的网贷产品！'])
            if title == '':
                title = ''.join(['来自', platform, '的网贷产品！'])

            summoney = float(summoney.replace(' ', ''))
            if summoney > 500000:
                indexSum = 5
            elif summoney > 200000:
                indexSum = 4
            elif summoney > 100000:
                indexSum = 3
            elif summoney > 10000:
                indexSum = 2
            else:
                indexSum = 1

            marktime = int(limitTime)  # 爬取时先变成数值
            if marktime <= 1:
                indexTime = 1
            elif marktime <= 6:
                indexTime = 2
            elif marktime <= 12:
                indexTime = 3
            else:
                indexTime = 4

            try:
                markrate = float(rate.replace('%', ''))
            except:
                markrate = 10
            if markrate <= 10:
                indexrate = 1
            elif markrate <= 15:
                indexrate = 2
            elif markrate <= 20:
                indexrate = 3
            else:
                indexrate = 4

            csvlist.append([title, platform, url, summoney, limitTime, \
                            rate, process, peoplenum, \
                            heatValue, description, indexSum, \
                            indexTime, indexrate])
        print 'writing...'

        if tlock!=None:
            if tlock.acquire():
                out_bidlist = open(self.rootpath + 'wdlist/db_bidlist.csv', 'ab')
                writer = csv.writer(out_bidlist)
                writer.writerows(csvlist)
                out_bidlist.close()
            tlock.release()
        if mlock!=None:
            if mlock.acquire():
                out_monitor = open(self.rootpath + 'wdlist/db_monitor.csv', 'ab')
                writer = csv.writer(out_monitor)
                writer.writerows([[platform, self.count_req, self.count_suc]])
                out_monitor.close()
            mlock.release()

        if iserror==True:
            if elock!=None:
                if elock.acquire():
                    out_error=open(self.rootpath+'wdlist/errorplatform.csv','ab')
                    writer=csv.writer(out_error)
                    writer.writerows([[platform,time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())]])
                    out_error.close()
                elock.release()

    def spider(self):
        pass

    def write_error(self):
        pass

    def nullpage(self,soup):
        errortitlelist=['Muse Proxy Server Error','ERRO: A URL requisitada',\
                        'Error Message']
        for each in errortitlelist:
            if each in soup.find('title').text:
                return False
        return True

class PaiPaiDai(P2P):

    def pagelist(self, soup, writebid=False):
        bidlist = []
        try:
            content = soup.find('div', {'class': 'wapBorrowList clearfix'}).findAll('ol', {'class': 'clearfix'})[1:]
        except:
            # print soup
            print 'lose one page...'
            return None
        for each in content:
            temp = each.find('div', {'class': 'w230 listtitle'}).find('a', {'class': 'title ell'})
            # print temp
            bid_url = temp['href']
            bid_title = temp.text.replace('...', '')
            bid_rate = each.find('div', {'class': 'w110 brate'}).text.replace('\r', '').replace('\n', '').strip()
            bid_sum = each.find('div', {'class': 'w90 sum'}).text.replace(u'¥', '').replace(',', '')
            bid_limitTime = each.find('div', {'class': 'w82 limitTime'}).text
            temp = each.find('div', {'class': 'w140 process'}).find('p').getText('&', '<br/>').split('&')
            bid_people = temp[0].replace(u'已有', '').replace(u'人投标', '')
            bid_process = temp[1].replace(u'已完成', '')

            bid_title = self.repchar(bid_title)
            bid_url = self.repchar(bid_url)
            bid_rate = self.repchar(bid_rate)
            bid_sum = self.repchar(bid_sum)
            bid_limitTime = self.repchar(bid_limitTime)
            bid_people = self.repchar(bid_people)
            bid_process = self.repchar(bid_process)
            # platform=repchar(platform)
            bid_decription = ''
            platform = '拍拍贷'
            bidlist.append([bid_title, bid_url, bid_rate, bid_sum, bid_limitTime, bid_people, bid_process, platform,
                            bid_decription])
        if writebid == True:
            outfile = open(self.rootpath + 'wdlist/temp.csv', 'ab')
            writer = csv.writer(outfile)
            writer.writerows(bidlist)
            outfile.close()
        return bidlist

    def spider(self, pagecounts=100):
        startPagelist = ['http://invest.ppdai.com/loan/list_safe_s0_p1?OldVersion=1&Rate=0',
                         'http://invest.ppdai.com/loan/list_riskmiddle_s0_p1?OldVersion=1&Rate=0', \
                         'http://invest.ppdai.com/loan/list_riskhigh_s0_p1?Rate=0']
        bidList = []
        error=False
        for startPage in startPagelist[:2]:#一个平台有多个列表
            nextPage = startPage
            iplist = self.getagent()
            c = 1
            while c <= pagecounts/len(startPagelist):
                #限制发出请的次数
                if self.count_req>self.maxrequestnums/len(startPagelist):
                    break
                self.count_req += 1
                print c
                ip = iplist[random.randint(1, len(iplist)) - 1]
                proxies = {
                    ip[2]: ip[2] + '://' + ip[0] + ':' + ip[1],
                }
                req = self.gethtml(nextPage, headers=self.headers, proxies=proxies,\
                                   timeout=self.timeout+60)
                if req == None:
                    continue
                soup = BeautifulSoup(req, 'lxml')
                if 'www.ppdai.com' not in str(soup):
                    # print soup
                    continue
                onepage = self.pagelist(soup)
                if onepage == None:
                    c+=1
                    error = True
                else:
                    c += 1
                    self.count_suc+=1
                    bidList.extend(onepage)
                try:
                    nextPage = 'http://invest.ppdai.com' + \
                               soup.find('div', {'class': 'pager'}).find('a', {'class': 'nextpage'})['href']
                except:
                    print 'soup is:',soup
                    print 'ppd nextpage not fund...'
                    break
                print 'nextpage:', nextPage
                if 'javascript' in nextPage:
                    print nextPage,'is useless!'
                    break
                if '?' not in nextPage:
                    print nextPage, 'is useless!'
                    break
                time.sleep(self.delay)
        return bidList,error

class WeiDai(P2P):
    def pagelist(self, soup):
        bidlist = []
        try:
            content = soup.find('div', {'class': 'list-content'}).findAll('dl', {'class': 'list-dl'})
        except:
            print 'lose one page...'
            return None
        for each in content:
            temp = each.find('dt').find('a')
            # print temp
            bid_url = 'https://www.weidai.com.cn' + temp['href']
            bid_title = temp.text
            # print each.find('dd',{'class':'clearfix'})
            temp = each.find('dd', {'class': 'clearfix'}).findAll('div', {'class': 'fl'})
            # print 'temp length',len(temp)
            bid_rate = temp[0].find('strong').text.replace('%', '')
            # print temp[2].find('em',{'class':'formatMoney'})
            bid_sum = temp[2].find('em', {'class': 'formatMoney'}).text.replace(u'元', '')
            bid_limitTime = temp[1].find('dt').text
            if u'天' in bid_limitTime:
                bid_limitTime = 1
            elif u'个月' in bid_limitTime:
                bid_limitTime = bid_limitTime.replace(u'个月', '')
            bid_people = ''
            bid_process = temp[5].find('div', {'class': 'meter'}).text.replace('%', '')
            bid_decription = temp[4].find('dt').text
            # print '----------------------------------------------------'
            # print 'title', bid_title
            bid_title = self.repchar(bid_title)
            bid_url = self.repchar(bid_url)
            bid_rate = self.repchar(bid_rate)
            bid_sum = self.repchar(bid_sum)
            bid_limitTime = self.repchar(bid_limitTime)
            bid_people = self.repchar(bid_people)
            bid_process = self.repchar(bid_process)
            bid_decription = self.repchar(bid_decription)
            platform = '微贷网'
            bidlist.append([bid_title, bid_url, bid_rate, bid_sum, bid_limitTime, bid_people, bid_process, platform,
                            bid_decription])

        return bidlist

    def spider(self, pagecounts=50):
        startPage = 'https://www.weidai.com.cn/bidlist/tenderList?page=1'
        nextPage = startPage
        bidList = []
        error =False
        c = 1
        iplist = self.getagent()
        while c < pagecounts:
            self.count_req += 1
            print c
            ip = iplist[random.randint(1, len(iplist)) - 1]
            proxies = {
                ip[2]: ip[2] + '://' + ip[0] + ':' + ip[1]  # "http://115.29.34.2:3128",
            }
            # print 'WeiDai IP:',proxies
            req = self.gethtml(nextPage, headers=self.headers, proxies=proxies)
            if req == None:#如果网页连接时间超时则重新打开
                continue
            soup = BeautifulSoup(req, 'lxml')
            # print soup

            onepage = self.pagelist(soup)
            if onepage == None:#如果打开网页出错爬虫被禁\网页改版等原因
                c+=1
                error=True
            else:
                c += 1
                self.count_suc+=1
                bidList.extend(onepage)
            nextPage = 'https://www.weidai.com.cn/bidlist/tenderList?page=' + str(c)
            print 'nextpage:', nextPage
            if 'javascript' in nextPage:
                break
            if '?' not in nextPage:
                break
            time.sleep(self.delay)

        return bidList,error

class LuJinSuo(P2P):
    def pagelist(self, soup):
        bidlist=[]
        try:
            content = soup.find('ul', {'class': 'main-list'}).findAll('li',
                                      {'class': 'product-list  clearfix         '})
        except:
            print 'lose one page...'
            return None
        for each in content:
            temp = each.find('dt', {'class': 'product-name'}).find('a')
            # print temp
            if 'http' not in temp['href']:
                bid_url='https://list.lu.com'+temp['href']
            else:
                bid_url = temp['href']
            bid_title = temp.text.replace('...', '')
            temp = each.find('dd')
            bid_rate = temp.find('li', {'class': 'interest-rate'}).find('p').text

            try:
                bid_limitTime = temp.find('li', {'class': 'invest-period'}).find('p').text
                bid_decription = '到期一次性还本付息'
                bid_process = each.find('div', {'class': 'progress'}).find('div', {'class': 'bar'})['style'].replace(
                    'width: ', '')
            except:
                bid_limitTime = temp.find('li', {'class': 'invest-insurance-comment'}).find('p').text
                bid_decription = ''
                bid_process = u'未知'
            if u'天' in bid_limitTime:
                bid_limitTime = int(bid_limitTime[:bid_limitTime.index(u'天')]) / 30
            bid_sum = each.find('div', {'class': 'product-amount'}).find('p').find('em').text.replace(',', '')
            bid_people = ''

            # print '----------------------------------------------------'
            # print 'title', bid_title
            bid_title = self.repchar(bid_title)
            bid_url = self.repchar(bid_url)
            bid_rate = self.repchar(bid_rate)
            bid_sum = self.repchar(bid_sum)
            bid_limitTime = self.repchar(bid_limitTime)
            bid_people = self.repchar(bid_people)
            bid_process = self.repchar(bid_process)
            platform='陆金所'
            bidlist.append([bid_title, bid_url, bid_rate, bid_sum, bid_limitTime, bid_people, bid_process, platform,
                            bid_decription])
        return bidlist

    def spider(self,pagecounts=50):
        startPagelist = ['https://list.lu.com/list/dingqi?currentPage=1']
        bidList=[]
        error=False
        for startPage in startPagelist:
            nextPage = startPage
            c = 1
            iplist = self.getagent()
            while c<=pagecounts/len(startPagelist):
                self.count_req+=1
                print c
                ip = iplist[random.randint(1, len(iplist)) - 1]
                proxies = {
                    ip[2]: ip[2] + '://' + ip[0] + ':' + ip[1]  # "http://115.29.34.2:3128",
                }

                # proxies = {'http': 'http://61.174.10.22:8080'}
                req = self.gethtml(nextPage, headers=self.headers, proxies=proxies)
                if req == None:
                    continue
                soup = BeautifulSoup(req, 'lxml')
                # print soup
                onepage=self.pagelist(soup)
                if onepage==None:
                    c+=1
                    error=True
                else:
                    c += 1
                    self.count_suc+=1
                    bidList.extend(onepage)
                if c > 4:
                    break
                # -----------------------change------------------------------
                nextPage = 'https://list.lu.com/list/dingqi?currentPage=' + str(c)

                time.sleep(self.delay)

        return bidList,error


class LanTouZi(P2P):
    def pagelist(self,soup):
        bidlist = []
        platform = '懒投资'
        try:
            content = soup.find('ul', {'class': 'project-list'}).findAll('li')
        except:
            print 'lose one page...'
            return None
        for each in content:
            temp = each.find('div', {'class': 'pro-head'}).find('a')
            # print temp
            bid_url = temp['href']
            bid_title = temp.text.replace('...', '')

            temp = each.find('div', {'class': 'project-info clearfix'})
            bid_rate = temp.find('div', {'class': 'info-one'}).find('p').text
            bid_limitTime = temp.find('div', {'class': 'info-two'}).find('p').find('em').text
            bid_sum = temp.find('div', {'class': 'info-three'}).find('p').find('em').text
            bid_decription = ''
            bid_process = ''

            if u'天' in bid_limitTime:
                bid_limitTime = int(bid_limitTime[:bid_limitTime.index(u'天')]) / 30
            bid_people = ''

            # print '----------------------------------------------------'
            # print 'title', bid_title
            bid_title = self.repchar(bid_title)
            bid_url = self.repchar(bid_url)
            bid_rate = self.repchar(bid_rate)
            bid_sum = self.repchar(bid_sum)
            bid_limitTime = self.repchar(bid_limitTime)
            bid_people = self.repchar(bid_people)
            bid_process = self.repchar(bid_process)

            # print bid_title, bid_url, bid_rate, bid_sum, bid_limitTime, bid_people, bid_process, platform, bid_decription
            bidlist.append([bid_title, bid_url, bid_rate, bid_sum, bid_limitTime, bid_people, bid_process, platform,
                            bid_decription])
            # map(lambda x:x.replace('\r', '').replace('\n', '').strip(),[bid_title,bid_url,bid_rate,bid_sum,bid_limitTime,bid_process,bid_people])
        return bidlist

    def spider(self, pagecounts=50):
        startPagelist = ['https://lantouzi.com/bianxianjihua/index?page=1&size=14']
        c = 1
        bidList = []
        for startPage in startPagelist:
            nextPage = startPage
            iplist = self.getagent()
            while c<pagecounts and c<20:
                self.count_req += 1
                print c
                ip = iplist[random.randint(1, len(iplist)) - 1]
                proxies = {
                    ip[2]: ip[2] + '://' + ip[0] + ':' + ip[1],# "http://115.29.34.2:3128",
                }

                req = self.gethtml(nextPage, headers=self.headers, proxies=proxies)
                if req == None:
                    continue
                soup = BeautifulSoup(req, 'lxml')
                # print soup
                onepage=self.pagelist(soup)
                c+=1
                if onepage!=None:
                    try:
                        bidList.extend(onepage)
                    except:
                        print onepage
                        continue
                # -----------------------change------------------------------
                # nextPage = "https://lantouzi.com/bianxianjihua/index?page=&size=14          "
                print 'c:',c
                nextPage = "https://lantouzi.com/bianxianjihua/index?page="+str(c)+"&size=14"
                print 'nextpage：',nextPage
                time.sleep(self.delay)
        self.count_suc = c
        return bidList,False


def runmain():
    coninfo = "psql -h 127.0.0.1 -p 5432 -U kun -d p2p"
    threads = []
    tempfilelock = threading.Lock()
    errorfilelock=threading.Lock()
    monitorlock = threading.Lock()

    # 爬取实时信息，多线程
    ppd = PaiPaiDai()
    wd = WeiDai()
    ljs=LuJinSuo()
    # ltz=LanTouZi()
    threads.append(threading.Thread(target=ppd.clandtocsv, args=(20, tempfilelock, monitorlock,errorfilelock)))
    threads.append(threading.Thread(target=wd.clandtocsv, args=(20, tempfilelock, monitorlock,errorfilelock)))
    threads.append(threading.Thread(target=ljs.clandtocsv,args=(10,tempfilelock, monitorlock,errorfilelock)))
    # threads.append(threading.Thread(target=ltz.clandtocsv, args=(5, tempfilelock, monitorlock,errorfilelock)))
    for i in range(len(threads)):
        threads[i].start()
    for i in range(len(threads)):
        threads[i].join()

    # 清空list_source,bidlist写入数据库表list_source
    os_Truncate = Template('''$count -c "Truncate table $table;"''')
    os.system(os_Truncate.substitute(count=coninfo, table='sp_reqinfo'))
    ppd.writetoDB_monitor()
    # 清空sp_reqinfo,监控信息写入数据库表sp_reqinfo
    os.system(os_Truncate.substitute(count=coninfo, table='list_source'))
    ppd.writetoDB_list()

    # 更新list
    os.system(os_Truncate.substitute(count=coninfo, table='list'))  # 清空list
    os_ex2 = '''$count -c "insert into $table2(id,title,platform,url,sum,limittime,rate,
    process,peoplenum,heatvalue,decription,indexsum,indextime,indexrate,document)
    select $table1.*,
    setweight(to_tsvector('testzhcfg',list_source.title),'A')  ||
    setweight(to_tsvector('testzhcfg',list_source.decription),'B') as document
    from $table1;"'''
    os_ex2 = Template(os_ex2)
    os.system(os_ex2.substitute(count=coninfo, table2='list', table1='list_source'))  # 插入list
    # 删除零时文件
    os.system('rm {0}'.format('/home/chenkun/p2pdata/wdlist/db_bidlist.csv'))
    os.system('rm {0}'.format('/home/chenkun/p2pdata/wdlist/db_monitor.csv'))

if __name__ == '__main__':
    runcounts=0
    while 1:
        runcounts += 1
        print '第', runcounts, '次运行爬虫'
        runmain()
        print 'sleep......', getValue('runDelay'), 's'
        time.sleep(float(getValue('runDelay')))



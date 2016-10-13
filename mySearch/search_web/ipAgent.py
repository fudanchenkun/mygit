#! /usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import csv
from bs4 import BeautifulSoup

def testIp(ip,host,type):
  url='http://www.ip.cn'
  if type=='http':
    proxies = {"http": "http://"+(':').join([ip,host]),}
  else:
    proxies = {"https": "http://" + (':').join([ip,host]),}
  try:
    html=requests.get(url,proxies=proxies,timeout=2)._content
    print proxies,'useful'
    soup=BeautifulSoup(html)
    # print proxies
    # print soup.find('div',{'id':'result'}).text
    return True
  except:
    print ip, 'bad'
    return False

def getIp(url,header,page):
  #page 翻页
  print url
  ipList = []
  for i in range(1,page+1):
    html=requests.get(url=url+str(i),headers=header)
    soup=BeautifulSoup(html._content,'lxml')
    content=soup.find('table',{'id':'ip_list'}).findAll('tr',{'class':'odd'})
    for i in range(1,len(content)):
      # print content[i]
      temp = content[i].findAll('td')
      v1=temp[6].find('div').find('div')['style'].replace('width:','').replace('%','')
      v2=temp[7].find('div').find('div')['style'].replace('width:','').replace('%','')
      timelong = temp[8].text
      if u'天' in timelong:
        if int(v1)>60 and int(v2)>60 and int(timelong.replace(u'天',''))>1:
          ip=temp[1].text
          host=temp[2].text
          type=temp[5].text.lower()
          if testIp(ip,host,type)==True:
            ipList.append((ip,host,type))
    if len(ipList)>10:
      break
  return ipList

def agentfresh(page=5):
  root = '/home/chenkun/p2pdata/ipagent/'
  xcHead='http://www.xicidaili.com/'
  xcUrl=[xcHead+'nn/',xcHead+'nt/',xcHead+'wn/',xcHead+'wt/']
  header={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
  }
  allIp=[]
  for each in xcUrl:
    allIp.extend(getIp(each,header,page))
  # print allIp
  outfile=open(root+'ipagent_new.csv','wb')
  writer=csv.writer(outfile)
  writer.writerows(allIp)
  outfile.close()
  return



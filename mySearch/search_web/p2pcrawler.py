#! /usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
class P2pCrawler(object):
    def __init__(self,entrance=None,kwlist=None):
        self.entrance=entrance
        self.kwlist=kwlist
        self.headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}

    def gethtml(self,url,timeout=2):
        try:
            req=requests.get(2,headers=self.headers,timeout=timeout)
        except:
            return None
        return req._content

    def gethref(self,html):
        if self.gethtml(self.entrance)==None:
            return None
        hreflist=[]
        soup=BeautifulSoup(html,"lxml")
        temp=soup.find_all('a')
        for url in temp:
            if 'href' in url.attrs.keys() and 'javascript' not in url['href']:
                if 'http' in url['href'] :
                    hreflist.append(url['href'])
                else:
                    hreflist.append(''.join(['http://www.wdzj.com',url['href']]))
        return hreflist

if __name__ == '__main__':
    cw=P2pCrawler('http://www.wdzj.com/',['wdzj'])

import requests
from bs4 import BeautifulSoup
import time
import csv

def gethtml(url):
    headers = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
    try:
        result = requests.get(url, headers=headers)
        print result._content
    except:
        return None

    return result._content

def repchar(strtext):
    return unicode(strtext).replace(' ','').replace(',',' ').replace('\n',' ').replace('\r',' ')\
        .replace('  ','').strip().encode('utf-8')

def newsinfo(url):
    html=gethtml(url)
    if html==None:
        return None
    soup = BeautifulSoup(html, "lxml")
    temp=soup.find('div',{'class':'con_news'})
    head=soup.find('head')
    info=range(8)
    try:
        info[0]=head.find('title').text
        info[1]=head.find('meta',{'name':'keywords'})['content']
        info[2]=head.find('meta',{'name':'description'})['content']

        info[3]=temp.find('h1').text#newstitle
        info[4]=temp.find('ul').find('li',{'class':'n_time'}).text#newstime
        info[5]=temp.find('ul').find('li',{'class':'news_con_p'}).text#newscontent
        info[6]=''.join([info[5][:150],'......'])#part news
        info[7]=url
        # print info
    except:
        print 'bad'
        return None
    return map(repchar,info)

def getnewslist(listurl):
    html=gethtml(listurl)
    soup=BeautifulSoup(html,"lxml")
    try:
        temp2=soup.find('div',{'class':'sideLeft'}).find('div',{'class':'nbs_2'})
        temp=temp2.findAll('li')
        newsurl_list=[]
        for li in temp:
            newsurl_list.append(li.find('a', {'class': 'news_til'})['href'])
    except:
        return None
    return newsurl_list

if __name__ == '__main__':
    xifen_dic={'shuju':23,'licai':85,'guowai':26,'guandian':40,\
               'jiedai':98,'jinrong':138,'yybb':82,'gundong':1120}
    xifen_name='gundong'
    pagelen=1120
    path='/home/chenkun/p2pdata/wdnews/'
    filename=xifen_name+'_news.csv'
    url_head = 'http://www.wdzj.com/news/'+xifen_name+'/p'  # http://www.wdzj.com/news/hangye/p1.html
    url_end = '.html'

    newslist=[]
    outfile = open(''.join([path,filename]), 'ab')
    writer = csv.writer(outfile)
    for i in range(1,pagelen+1):
        print i
        url=''.join([url_head,str(i),url_end])
        # print url
        nl=getnewslist(url)
        if nl!=None:
            for each in nl:
                news=newsinfo(each)
                if news!=None:
                    newslist.append(news)
                if len(newslist)>100:
                    break
                    writer.writerows(newslist)
                    newslist=[]
        else:
            print 'list is bad!!!:',i
    writer.writerows(newslist)
    outfile.close()


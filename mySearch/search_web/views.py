#coding=utf-8
import os,csv,time
from django.shortcuts import render
from django.http import HttpResponse
from models import News,List,SpReqinfo
from django.core.paginator import Paginator
from django.db import connection
from P2pClass import *
from xmlsetting import alterxml,getValue

# from models import ppd_show
from django.db.models import Model

# Create your views here.

def cutkeywords(keywords):
    cursor = connection.cursor()
    cursor.execute("select to_tsvector('testzhcfg',%s)", [keywords])
    cutstr=cursor.fetchone()[0]

    if ',' in cutstr:#处理分词后的格式问题
        cutstr=cutstr.split(',')[0]
    print 'kw:', cutstr, '-----------'
    kw = '&'.join(eval('{' + cutstr.replace('("', '').strip().replace(' ', ',') + '}').keys())
    # if len(keywords) > 2:
    #     cursor = connection.cursor()
    #     cursor.execute("select to_tsvector('testzhcfg',%s)", [keywords])
    #     kw = '&'.join(eval('{' + cursor.fetchone()[0].replace('("', '').strip().replace(' ', ',') + '}').keys())
    # else:
    #     print 'keywords length < 2', keywords
    #     kw = keywords
    return kw

def index(request,selType=3):
    keywords = request.GET.get('keywords', '')
    # keywords=keywords.replace('&',' ').strip()
    print 'keywords:',keywords
    sum = request.GET.get('sum','0')
    timelong = request.GET.get('timelong','0')
    rate = request.GET.get('rate','0')
    if sum=='0':
        sumsql=','.join(map(str,range(1,6)))
    else:
        sumsql=sum
    if timelong=='0':
        timelongsql=','.join(map(str,range(1,5)))
    else:
        timelongsql=timelong
    if rate=='0':
        ratesql=','.join(map(str,range(1,5)))
    else:
        ratesql=rate
    print sum,timelong,rate
    # print 'keywords',keywords
    limit=5
    #选择读取数据的方法
    if selType==1:
        pass
    elif selType==2:
        #这样写有sql注入的风险
        sqlquery='''select * from ppd_show
        where indexsum in (%s)
        and indextime in  (%s)
        and indexrate in (%s)
        and title like %s
        order by heatvalue desc limit 100'''%(sumsql,timelongsql,ratesql,'%s')
        # 一定要切片，否则运行出错
        # sql内若有%要写成%%
        # 列表里的参数自带''
    elif selType==3:
        kw=cutkeywords(keywords)
        print 'kw:',kw
        if keywords=='':
            sqlquery = '''select * from list
            where indexsum in (%s)
            and indextime in  (%s)
            and indexrate in (%s)
            order by heatvalue desc limit 100''' % (sumsql, timelongsql, ratesql)
            # ppd = PpdShow.objects.raw(sqlquery)[:100]
            listdata=List.objects.raw(sqlquery)[:100]
        else:
            sqlquery='''select * from list
            where indexsum in (%s)
            and indextime in  (%s)
            and indexrate in (%s)
            and list.document @@ to_tsquery(%s)
            order by heatvalue desc limit 100'''%(sumsql,timelongsql,ratesql,'%s')
            # ppd = PpdShow.objects.raw(sqlquery, [kw])[:100]
            listdata = List.objects.raw(sqlquery, [kw])[:100]

    paginatior=Paginator(listdata,limit)
    page=request.GET.get('page',1)
    loaded=paginatior.page(page)

    result={
        "keywords":keywords.replace('&nbsp;',' '),
        "sum":sum,
        "timelong":timelong,
        "rate":rate,
        "info":loaded,
    }
    return render(request,'index.html',result)

def news(request):
    keywords = request.GET.get('keywords', 'p2p网贷')
    kw=cutkeywords(keywords)
    print 'kw',kw
    sqlquery='''select news.id,news.page_title,news.news_url,news.news_part
    from news
    where news.document @@ to_tsquery(%s)
    '''
    print sqlquery
    # newsdata = News.objects.all()[:100]
    newsdata=News.objects.raw(sqlquery,[kw])[:]

    paginatior=Paginator(newsdata,10)
    page=request.GET.get('page',1)
    loaded=paginatior.page(page)

    result={
        "keywords":keywords,
        "info": loaded,
        # "info":newsdata,

    }
    return render(request,'news.html',result)

def bidSearch(request):
    limit=5
    keywords=request.GET['searchINput']
    ppd=PpdShow.objects.filter(title_contains=keywords)[:100].order_by('heatvalue')

    paginatior = Paginator(ppd, limit)
    page = request.GET.get('page', 1)
    loaded = paginatior.page(page)

    result = {
        "info": loaded,
    }
    return render(request,'index.html',result)

def semanticweb(request):
    return render(request,'semanticwb.html')

def spmonitor(request):
    s=getValue('spiderDelay')
    r=getValue('runDelay')
    result={'spiderDelay':s,'runDelay':r,}
    return render(request,'spmonitor.html',result)

from django.http import JsonResponse

def sptest(request):
    pt=request.GET.get('pt',None)
    if pt not in ['PaiPaiDai','WeiDai','LuJinSuo','LanTouZi']:
        pt=None
    if pt==None:
        print '无参数。。。'
        return JsonResponse([['暂无数据，该平台数据还在获取中，敬请期待！']], safe=False)
    pt=eval(pt+'()')
    print '原始发出请求次数:', pt.count_req
    a,t=pt.spider(6)
    # print 'from wedai:\n',a
    print '发出请求次数:',pt.count_req

    return JsonResponse(a, safe=False)

def ajax_list(request):
    a=[]
    try:
        infile = open('/home/chenkun/p2pdata/wdlist/temp.csv', 'r')
    except:
        print 'return []'
        time.sleep(2)
        return JsonResponse(a, safe=False)
    for each in csv.reader(infile):
        a.append(each)
    # print a
    infile.close()
    print 'a response'
    time.sleep(3)
    return JsonResponse(a, safe=False)

def spider_test(request):
    time.sleep(5)
    print '获取数据。。。'
    ppd=PaiPaiDai()
    ppd.spdier(20,True)
    time.sleep(5)
    os.system('rm {0}'.format('/home/chenkun/p2pdata/wdlist/temp.csv'))
    return HttpResponse()

def echarts_req(request):
    ereq=SpReqinfo.objects.all()
    a={}
    a['platform'] = []
    a['percent'] = []
    for each in ereq:
        a['platform'].append(each.platform.strip())
        if each.count_req!=0:
            a['percent'].append(float(each.count_suc)*100/each.count_req)
    #a不需转化为json
    return JsonResponse(a,safe=False)

def xml_alter(request):
    print 'yes....'
    alterdic={}
    spiderDelay=request.GET.get('p1','')
    runDelay=request.GET.get('p2','')
    timeout=request.GET.get('p3','')
    if spiderDelay!='':
        alterdic['spiderDelay']=spiderDelay
    if runDelay!='':
        alterdic['runDelay']=runDelay
    if timeout!='':
        alterdic['timeout']=timeout
    if len(alterdic)>0:
        alterxml(alterdic)
    else:
        print '无需更新setting'
    return HttpResponse()

def spider_run(request):
    print 'spider run....'
    runmain()
    return HttpResponse()

def error_spider(request):
    print 'run error-spider'
    errorfile=open('/home/chenkun/p2pdata/wdlist/errorplatform.csv', 'r')
    csvlist=[]
    for line in errorfile:
        csvlist.append(line)
    errorfile.close()

    return JsonResponse(csvlist,safe=False)

from ipAgent import agentfresh
def agent_fresh(request):
    print 'fresh agent...'
    page=5#翻页
    agentfresh(page)
    return HttpResponse()
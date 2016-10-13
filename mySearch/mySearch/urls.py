"""mySearch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from search_web.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/',index),
    url(r'^news/',news),
    url(r'^semanticwb/',semanticweb),
    url(r'^spmonitor/',spmonitor),
    url(r'^ajax_list/$', ajax_list, name='ajax-list'),
    url(r'^spider_test/$', spider_test, name='spider-test'),
    url(r'^sptest/$',sptest, name='sp-test'),
    url(r'^echarts_req/$', echarts_req, name='echarts-req'),
    url(r'^xml_alter/$', xml_alter, name='xml-alter'),
    url(r'^spider_run/$',spider_run,name='spider_run'),
    url(r'^error_platform/$',error_spider,name='error-platform'),
    url(r'^agent_fresh/$',agent_fresh,name='agent-fresh')
]

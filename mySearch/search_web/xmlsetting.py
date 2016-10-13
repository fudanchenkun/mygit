#! /usr/bin/env python
# -*- coding: utf-8 -*-

from xml.dom import minidom#生成xml文件
import xml.etree.cElementTree as ET#解析xml

def write_xml(xmlstr):
    f=file('/home/chenkun/p2pdata/spsetting.xml','w')
    f.write(xmlstr)
    f.close()

def setxmlDefault():
    setdic={'spiderDelay':[0,'爬取爬虫间隔'],'runDelay':[60,'实时运行间隔'],\
            'timeout':[2,'请求连接超时阈值']}
    doc=minidom.Document()
    rootNode=doc.createElement('setting')
    doc.appendChild(rootNode)
    for key,values in setdic.items():
        newnode=doc.createElement(key)
        value=doc.createElement('value')
        value.appendChild(doc.createTextNode(str(values[0])))
        description=doc.createElement('description')
        description.appendChild(doc.createTextNode(values[1]))
        newnode.appendChild(value)
        newnode.appendChild(description)
        rootNode.appendChild(newnode)
    f=open('/home/chenkun/p2pdata/spsetting.xml','w')
    doc.writexml(f)
    f.close()

def getValue(key):
    root=ET.parse('/home/chenkun/p2pdata/spsetting.xml')
    return root.find(key).find('value').text.strip()

def alterxml(tdic):
    root=ET.parse('/home/chenkun/p2pdata/spsetting.xml')#读入
    for key in tdic.keys():
        node=root.find(key)
        node.remove(node.find('value'))
        e=ET.Element('value')
        e.text=tdic[key]
        node.insert(2,e)
        # root.remove(root.find(key).find('value'))
        # root.find()
    root.write('/home/chenkun/p2pdata/spsetting.xml','utf-8', True)

if __name__ == '__main__':
    setxmlDefault()


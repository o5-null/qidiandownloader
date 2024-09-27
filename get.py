import re

import cn2an
import Levenshtein#莱文斯坦距离 检查文本相似度
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from gne import GeneralNewsExtractor
from goose3 import Goose
from goose3.text import StopWordsChinese
from readability import Document
from loguru import logger


extractor = GeneralNewsExtractor()
g = Goose({'stopwords_class': StopWordsChinese})

#readability提取器
def clean_readability(data:str): #获取网站正文文本
    logger.debug('调用readability url:'+data.url)
    try:
        doc = Document(data.content)
        html = doc.summary()
        #获取页面标题
        title = doc.title()
        #对html进行修正以使img正常加载
        need = '<figure class="img-box" contenteditable="false">'
        html = html.replace(need,'<figure>')
        need = '<figure contenteditable="false" class="img-box">'
        html = html.replace(need,'<figure>')
        html = html.replace('data-src','src')
        html = html.replace('src="//','src="https://')
        #获取txt格式
        txt = doc.summary().replace('</p>','\n')#doc.summary()为提取的网页正文但包含html控制符，这一步是替换换行符
        txt = re.sub(r'</?\w+[^>]*>', '', txt)      #这一步是去掉<****>内的内容
        txt = txt.replace('&nbsp;','')
        #创个字典存放数据
        fine = {}
        fine['title'] = title
        fine['html'] = html
        fine['txt'] = txt
    except:
        #创个字典存放数据
        fine = {}
        fine['title'] = 'null'
        fine['html'] = 'null'
        fine['txt'] = 'null'
        return fine
    return fine

#GNE提取器
def clean_gne(data):
    logger.debug('调用GNE url:'+data.url)
    doc = extractor.extract(data.content.decode('UTF-8'))
    print(doc)
    #创个字典存放数据
    fine = {}
    fine['title'] = doc['title']
    fine['html'] = data
    fine['txt'] = doc['content']
    return fine

#Goose3提取器
def clean_goose3(data):
    logger.debug('调用Goose3 url:'+data.url)
    doc = g.extract(raw_html=data.content.decode('UTF-8'))
    #创个字典存放数据
    fine = {}
    fine['title'] = doc.title
    fine['html'] = data
    fine['txt'] = doc.cleaned_text
    return fine

#提取章节数字
def get_num(title:str):
    a = re.search('([―－\-─—壹贰叁肆伍陆柒捌玖一二两三四五六七八九十○〇零百千O0-9０-９]{1,12})',title)
    if title.find('番外'):#不匹配则为NoneType
        return 0
    a =a.group(1)
    if not a.isdigit():#非阿拉伯数字
        a = cn2an.transform(a)#转化
    else:
        return int(a)
    return int(a)

#排除重复章节
def chaptor_list_claen(list):
    new_list = []#创建临时列表
    num_list = []
    for a in list:
        if a == 'null':
            continue
        #a.append(get_num(a))#添加章节数字索引
        if not a[-1] in num_list or a[-1] == 0:
            num_list.append(a[-1])
            new_list.append(a)
    new_list_num = sorted(new_list,key=lambda e:e[-1])
    return new_list_num

#提取章节超链接
def get_chaptor_list(data) -> dict:
    """
    提取章节超链接
    返回 {'title':str,'chapter_list':[[章节url,章节名]]}
    """
    #获取一级域名拼接超链接
    url = urlparse(data.url)
    #尝试提取标题
    title = clean_readability(data)['title']
    soup = BeautifulSoup(data.content, features='html5lib')
    tags = soup.find_all('a')
    chapter_list = []
    for tag in tags:
        a = re.search('(第)([―－\-─—壹贰叁肆伍陆柒捌玖一二两三四五六七八九十○〇零百千O0-9０-９]{1,12})(章|节|回|集|部|卷|篇)(.*)',tag.text)
        if a:#不匹配则为NoneType
            if re.match('/',str(tag.get('href'))):#如果链接没有一级域名
                chaptor_one_url = url.scheme+'://'+url.netloc+str(tag.get('href'))
            chapter_list.append([chaptor_one_url,tag.text,get_num(tag.text)])
    chapter_list = chaptor_list_claen(chapter_list)#去除重复章节
    logger.debug('获取目录 共'+str(len(chapter_list))+'章')
    return {'title':title,'chapter_list':chapter_list}

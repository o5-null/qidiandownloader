from w3lib.url import canonicalize_url
import re
import difflib
import Levenshtein as ls#莱文斯坦距离 检查文本相似度
#url相似度识别算法
def diff(sample:list,url:str):#根据已经获取的url检查目标url相似度
    def create_string_serial(need_url:str):#对url序列化
        need_url = canonicalize_url(need_url)#url规范化
        need_url.replace('https://','')
        need_url.replace('http://','')
        need_url.split('/')
        return need_url

    def calculate_weighted_sequence(sample_url:str,url:str):
        similarity_level = []
        sample_url = create_string_serial(sample_url)#序列化
        url = create_string_serial(url)
        bigger_len = lambda x, y: x if x > y else y#返回较大的值
        for i in range(bigger_len(len(sample_url), len(url))):
            similar.append(ls.distance(sample_url[i],url[i]))

    similar = []
    for sam_url in sample:
        sam_url = canonicalize_url(sam_url)
        url = canonicalize_url(url)
        #similar.append(ls.jaro_winkler(sam_url,url))
        similar.append(difflib.SequenceMatcher(None,sam_url,url).quick_ratio())
    print(similar)

sam = ['Https://www.biquge.co/2_2292/879982.html',
       'https://www.biquge.co/2_2292/880007.html',
       'https://www.biquge.co/2_2292/880016.html',
       'https://www.biquge.co/2_2292/880100.html',
       'https://www.biquge.co/2_2292/880173.html']


diff(sam,'https://www.biquge.co/dushixiaoshuo/')
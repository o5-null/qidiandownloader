from yarl import URL
import re
import difflib
import Levenshtein as ls#莱文斯坦距离 检查文本相似度
#url相似度识别算法
def diff(sample:list,url:str):#根据已经获取的url查找类似url
    url = re.sub('https*','',url.lower())
    url = url.replace('.','')
    url = url.replace('/','')
    url = url.replace(':','')
    similar = []
    for sam_url in sample:
        
        #去除无效字符
        sam_url = re.sub('https*','',sam_url.lower())
        sam_url = sam_url.replace('.','')
        sam_url = sam_url.replace('/','')
        sam_url = sam_url.replace(':','')
        similar.append(ls.jaro_winkler(sam_url,url))
        #similar.append(difflib.SequenceMatcher(None,sam_url,url).quick_ratio())
    print(similar)

sam = ['Https://www.biquge.co/2_2292/879982.html',
       'https://www.biquge.co/2_2292/880007.html',
       'https://www.biquge.co/2_2292/880016.html',
       'https://www.biquge.co/2_2292/880100.html',
       'https://www.biquge.co/2_2292/880173.html']
diff(sam,'https://www.biquge.co/dushixiaoshuo/')
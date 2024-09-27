from yarl import URL
import difflib
#url相似度识别算法
def diff(get:list,url:str):#根据已经获取的url查找类似url
    #对url进行切割
    a = URL(url)
    a = str(a.path).replace('\\',' ')
    print(simhashes)

diff('https://www.biquge.co/2_2292/15607964.html')
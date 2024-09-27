import requests
import re
import get

from bs4 import BeautifulSoup
headers ={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}
headers_phone = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; PRA-AL00X Build/HONORPRA-AL00X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/6.2 TBS/045714 Mobile Safari/537.36'
    }
a = re.search('第([―－\-─—壹贰叁肆伍陆柒捌玖一二两三四五六七八九十○〇零百千O0-9０-９]{1,12})[章|节|回|集|部|卷|篇]',title[1])
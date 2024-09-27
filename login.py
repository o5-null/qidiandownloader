from selenium import webdriver
from selenium.webdriver.common.by import By
from pathlib import Path
import json
import time
from loguru import logger

driver = webdriver.Chrome()
option = webdriver.ChromeOptions()  # 默认Chrome浏览器
# 关闭开发者模式, window.navigator.webdriver 控件检测到你是selenium进入，若关闭会导致出现滑块并无法进入。
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_argument('--disable-blink-features=AutomationControlled')
# option.add_argument('headless')               # Chrome以后台模式进行，注释以进行调试
# option.add_argument('window-size=1920x1080')  # 指定分辨率
option.add_argument('no-sandbox')             # 取消沙盒模式
option.add_argument('--disable-gpu')          # 禁用GPU加速
option.add_argument('disable-dev-shm-usage')  # 大量渲染时候写入/tmp而非/dev/shm
#执行js文件去除webdriver特征值（过不了滑块
with open('stealth.min.js') as f:
    js = f.read()

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": js
    })

driver.get('https://www.qidian.com')

if Path('./cookies.txt').exists():#如果cookies文件存在
    a = json.loads(Path('cookies.txt').read_text())
    for b in a:#遍历添加
        driver.add_cookie(b)
else:
    cookies = driver.get_cookies()
    Path('./cookies.txt').write_text(json.dumps(cookies))
print('登录成功')
driver.get('https://www.qidian.com')
time.sleep(5)
user_name = driver.find_element_by_id("user-name")#获取用户名
input()

def start_chrome(url:str): #开启chrome窗口，登陆账户
    driver.get(url)
    logger.debug('selenium访问'+url)

    if Path('./cookies.txt').exists():#如果cookies文件存在
        logger.debug('cookies文件存在')
        a = json.loads(Path('cookies.txt').read_text())
        for b in a:#遍历添加
            driver.add_cookie(b)
    else:#如果不存在则持续监测是否登陆
        cookies = driver.get_cookies()
        Path('./cookies.txt').write_text(json.dumps(cookies))
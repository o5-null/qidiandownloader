import requests

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import nicegui
from nicegui import ui
from nicegui import app

import get
headers ={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}
headers_phone = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; PRA-AL00X Build/HONORPRA-AL00X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/6.2 TBS/045714 Mobile Safari/537.36'
    }
brower = requests.Session() #创建浏览器
cookies = {'cookies': 'newstatisticUUID=1718075954_1918081557; fu=88581906; _yep_uuid=ba1e107a-8a44-3fbf-1ffa-4c1efa5f583a; Hm_lvt_f00f67093ce2f38f215010b699629083=1718075954; _gid=GA1.2.1630623734.1718075955; ywkey=ywuPIewIskYR; ywguid=1517808818; ywopenid=C9021D95E59C6A307E8245F4214A3B51; supportWebp=true; traffic_search_engine=; se_ref=; trkf=1; supportwebp=true; traffic_utm_referer=https%3A//www.google.com/; e2=%7B%22l6%22%3A%22%22%2C%22l1%22%3A%22%22%2C%22pid%22%3A%22qd_P_daoliu%22%2C%22eid%22%3A%22%22%7D; e1=%7B%22l6%22%3A%22%22%2C%22l1%22%3A%22%22%2C%22pid%22%3A%22qd_P_daoliu%22%2C%22eid%22%3A%22qd_A_mall_zhuomiandownload%22%2C%22l7%22%3A1%7D; _csrfToken=be60879a-cc11-4c1a-90c0-513bc390df50; Hm_lpvt_f00f67093ce2f38f215010b699629083=1718082515; _ga_FZMMH98S83=GS1.1.1718079677.2.1.1718082515.0.0.0; _ga=GA1.1.2089634908.1718075955; _ga_PFYW0QLV3P=GS1.1.1718079677.2.1.1718082515.0.0.0; w_tsfp=ltvgWVEE2utBvS0Q6KLpk06nEzg7Z2R7xFw0D+M9Os09CKMpUZqA2Id7uNfldCyCt5Mxutrd9MVxYnGJVt4meBAdRcWTb5tH1VPHx8NlntdKRQJtA5/eClUWKrl16mFBLz5eLETnij14I9JBxLEyglletXJx37ZlCa8hbMFbixsAqOPFm/97DxvSliPXAHGHM3wLc+6C6rgv8LlSgS3A9wqpcgQ2Xusewk+A1SgfDngj4RG7dOldNRytI86vWO0wrTPzwjn3apCs2RYx/UJk6EtuWZaxhCfAPSdAJlhvbFjhgbkgLa7+PuAkuzIfVKxGQQsV+Fkcs+c86wk='}
#a = requests.get('https://www.qidian.com/ajax/book/category?_csrfToken=be60879a-cc11-4c1a-90c0-513bc390df50&bookId=1038863996&w_tsfp=ltvgWVEE2utBvS0Q6KLpk06nEzg7Z2R7xFw0D%2BM9Os09CKMpUJuF14R6vtfldCyCt5Mxutrd9MVxYnGJVt4neBETQ82Vb5tH1VPHx8NlntdKRQJtA5%2FeClUWKrl16mFBLz5eLETnij14I9JBxLEyglletXJx37ZlCa8hbMFbxl0yufqB0Jtsez%2BYyw6FRUDKI2EKfeCevf5z28MDtH2KgQSgeQVhAM4QhUOS3S8WX2VwshC6ae0ONE2wKs78WPA1rDChkTr%2BasT63BY241Zl70Fme4Hh2kHLL3VMKA1obFG0kKI2Kvz1aaR46G0LVr5PSVkVqQ8ZteI5%2BURPDSi9YHWPBfp6tQAARvJZ%2F82seTnZxMm0dVsCq5hzh1El7cQBu2p2NTz%2BKd1aGWPMNicHKIsAbZ%2BzNSg0VhBXW2Zeqw%3D%3D',headers=headers,cookies=cookies)
#print(a.content.decode("utf-8","ignore"))


#当按下启动按钮
def start_get_novel():
    #获取url
    chaptor_url = url.value
    print(chaptor_url)
    html_data = brower.get(chaptor_url,headers=headers)#发送请求
    chaptor_list = get.get_chaptor_list(html_data)#获取章节超链接
    ui.notify(chaptor_list['title']+' 共 '+str(len(chaptor_list['chapter_list']))+' 章节')
    title.text = '共'+str(len(chaptor_list['chapter_list']))+'章节'
    with down_list:
        down_novel_title = ui.expansion(chaptor_list['title'])
        with down_novel_title:
            columns = [
                {'name': 'chapter_name', 'label': '章节名','field': 'chapter_name', 'required': True, 'align': 'left'}
            ]
            rows = []
            for a in chaptor_list['chapter_list']:
                rows.append({'chapter_name':a[1],'url':a[0]})
            table = ui.table(columns=columns, rows=rows, row_key='chapter_name', selection='multiple')
            with table:
                with table.add_slot('top-right'):
                    with ui.input(placeholder='搜索').props('type=search').bind_value(table, 'filter').add_slot('append'):
                        ui.icon('search')
            #ui.label().bind_text_from(table, 'selected', lambda val: f'Current selection: {val}')
            for down_novel_list in down_list:
                for down_chapter_list in down_novel_list:
                    if type(down_chapter_list) == nicegui.elements.table.Table:
                        pass
            ui.button('删除选中项', on_click=lambda: table.remove_rows(*table.selected)).bind_visibility_from(table, 'selected', backward=lambda val: bool(val))

#下载
def down():
    #检查当前下载列表中的小说
    for down_novel_list in down_list:#搜索下载列表中的小说
        for down_chapter_list in down_novel_list:
            if type(down_chapter_list) == nicegui.elements.table.Table:#找到表格对象
                print(down_chapter_list.rows)
                for down_chapter_url in down_chapter_list.rows:#遍历章节
                    pass


#创建分页
with ui.splitter(value=30).classes('w-full h-56') as splitter:
    with splitter.before:
            tabs = ui.tabs().props('vertical').classes('w-full')
            with tabs:
                main_page = ui.tab('主页',icon='home')
                down_page = ui.tab('下载列表')
                set_page = ui.tab('设置')
    with splitter.after:
        with ui.tab_panels(tabs, value=main_page).classes('w-full').props('vertical').classes('w-full h-full'):
            with ui.tab_panel(set_page):
                set_page_card = ui.card()#设置容器
                with set_page_card:
                    #选择解析引擎
                    engine = ui.select({'readability': 'Readability引擎','GNE':'GNE引擎','Goose3':'Goose3引擎'},value='readability')
            with ui.tab_panel(main_page):
                main_page_card = ui.card()#主页容器
                with main_page_card:
                    title = ui.label('标题')
                    #输入链接
                    url = ui.input('链接',placeholder='输入需处理链接').props('clearable')
                    #启动解析
                    ui.button('启动解析',on_click=start_get_novel)
            with ui.tab_panel(down_page):
                down_page_card = ui.card()#下载列表容器
                with down_page_card:
                    start_download = ui.button('开始下载',on_click=down)
                    down_list = ui.item()#下载列表
                    



ui.run(native=False)
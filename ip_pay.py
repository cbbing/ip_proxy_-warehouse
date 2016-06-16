#coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from selenium import webdriver
from bs4 import BeautifulSoup as bs
import os,time
import pandas as pd
from util.CodeConvert import GetNowTime
from config import engine

def get_ip_proxy():

    print 'start'
    # dir = 'C:\Users\Administrator\Downloads\\'
    # for parent, dirnames, filenames in os.walk(dir):
    #     for filename in filenames:
    #         if filename.endswith('.txt'):
    #             print filename
    #             try:
    #                 os.remove(dir + filename)
    #             except Exception,e:
    #                 print e

    # os.remove('C:\\Users\Administrator\\Downloads\\下载.txt')

    # fp = webdriver.FirefoxProfile()
    # fp.set_preference("browser.download.folderList", 2)
    # fp.set_preference("browser.download.manager.showWhenStarting", False)
    # fp.set_preference("browser.download.dir",os.getcwd())
    # fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/xml")

    dr = webdriver.PhantomJS()
    dr.get('http://www.daili666.net/web')
    tid = '**'
    dr.find_element_by_xpath('//input[@type="text" and @name="tid"]').send_keys(tid)
    # dr.find_element_by_xpath('//input[@type="text" and @name="num"]').send_keys('0')

    dr.find_element_by_xpath('//input[@type="radio" and @name="foreign" and @value="none"]').click()
    # dr.find_element_by_xpath('//input[@type="radio" and @name="download" and @value="true"]').click()
    dr.find_element_by_xpath('//input[@type="submit"]').click()

    for handle in dr.window_handles:
        dr.switch_to.window(handle)
        print dr.title
        if len(dr.title) == 0:
            break

    time.sleep(5)

    soup = bs(dr.page_source, 'lxml')
    data = soup.find('body').text
    #print data
    datas = data.split('\n')

    datas = [(d.split(':')[0], d.split(':')[1]) for d in datas if len(d.split(':'))==2]
    df = pd.DataFrame(datas, columns=['IP', 'Port'])
    df['Type'] = 'http'
    df['Anonymous'] = '高匿'
    df['Source'] = 'www.daili666.net'
    df['CreateTime'] = GetNowTime()
    df['UpdateTime'] = GetNowTime()
    print df.head()

    df.to_sql('ip_proxy_pay', engine, if_exists='replace', index=False)

    #备份
    df_free = pd.read_sql('select IP, Port from ip_proxy',engine)
    df_free['Port'] = df_free['Port'].astype(str)
    df_free['IP_Port'] = df_free['IP'] + ":" + df_free['Port']
    df['IP_Port'] = df['IP'] + ":" + df['Port']
    df = df[df['IP_Port'].apply(lambda x : x not in df_free['IP_Port'].get_values())]
    del df['IP_Port']
    print 'len:', len(df)
    df.to_sql('ip_proxy', engine, if_exists='append', index=False)

    # dr.quit()
    dr.close()
    print 'end'

if __name__ == "__main__":
    get_ip_proxy()



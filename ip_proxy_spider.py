# -*- coding:utf8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import os
import urllib
import time, datetime
import pexpect
import platform
import re
import pandas as pd
import requests

from bs4 import BeautifulSoup
from pandas import DataFrame
from subprocess import *
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Pool


from util.CodeConvert import *
from util.helper import fn_timer as fn_timer_
from config import engine, mysql_table_ip


class IP_Proxy_Spider:
    def __init__(self):

        self.count = 3
        self.wait_time = 5 # second
        self.ip_items = []
        self.dir_path = './data/'

        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36'}


    #
    def parse(self):
        #self.parse_haodaili()
        #self.parse_kuaidaili()
        self.parse_xici()

    # 好代理
    def parse_haodaili(self):

        def parse_one_page(url):
            try:
                r = requests.get(url, headers=self.headers, timeout=10)
                # page = urllib.urlopen(url)
                # data = page.read()
                soup = BeautifulSoup(r.text, "html5lib")
                #print soup.get_text()
                body_data = soup.find('table', attrs={'class':'content_table'})
                res_list = body_data.find_all('tr')
                for res in res_list:
                    each_data = res.find_all('td')
                    if len(each_data) > 3 and not 'IP' in each_data[0].get_text() and '.' in each_data[0].get_text():
                        item = IPItem()
                        item.ip = each_data[0].get_text().strip()
                        item.port = each_data[1].get_text().strip()
                        item.addr = each_data[2].get_text().strip()
                        item.type = each_data[3].get_text().strip()

                        print item.get_info()
                        if item.type.lower() == "http" or item.type.lower() == "https":
                            self.ip_items.append(item)
            except Exception,e:
                print e

        url_haodaili = 'http://www.haodailiip.com/guonei/{pid}'
        for i in range(1, self.count+1):
            url = url_haodaili.format(pid=i)
            parse_one_page(url)

            self._page_wait(i)

        print 'haodaili success: {} have get {} items'.format('\n', len(self.ip_items))

    # 快代理
    def parse_kuaidaili(self):

        def parse_one_page(url):
            try:
                r = requests.get(url, headers=self.headers, timeout=10)
                #page = urllib.urlopen(url)
                #data = page.read()
                soup = BeautifulSoup(r.text, "html5lib")
                print soup.get_text()
                body_data = soup.find('table', attrs={'class':'table table-bordered table-striped'})
                res_list = body_data.find_all('tr')
                for res in res_list:
                    each_data = res.find_all('td')
                    if len(each_data) > 3 and not 'IP' in each_data[0].get_text() and '.' in each_data[0].get_text():
                        item = IPItem()
                        item.ip = each_data[0].get_text().strip()
                        item.port = each_data[1].get_text().strip()
                        item.addr = each_data[4].get_text().strip()
                        item.type = each_data[3].get_text().strip().lower()
                        item.anonymous = each_data[2].get_text().strip()

                        print item.get_info()
                        if item.type == "http" or item.type == "https":
                            self.ip_items.append(item)
            except Exception,e:
                print e

        url_kuaidaili = 'http://www.kuaidaili.com/free/inha/{pid}/'
        for i in range(1, self.count+1):
            url = url_kuaidaili.format(pid=i)
            parse_one_page(url)

            self._page_wait(i)

        print 'kuaidaili success: {} have get {} items'.format('\n', len(self.ip_items))

    # 西刺代理
    def parse_xici(self):

        def parse_one_page(url):
            try:
                r = requests.get(url, headers=self.headers, timeout=10)
                soup = BeautifulSoup(r.text, "html5lib")
                print soup.get_text()
                body_data = soup.find('table', attrs={'id':'ip_list'})
                res_list = body_data.find_all('tr')
                for res in res_list:
                    each_data = res.find_all('td')
                    if len(each_data) > 6 and '.' in each_data[2].get_text():

                        item = IPItem()
                        item.ip = each_data[2].get_text().strip()
                        item.port = each_data[3].get_text().strip()
                        item.addr = each_data[4].get_text().strip()
                        item.type = each_data[6].get_text().strip().lower()
                        item.anonymous = each_data[5].get_text().strip()
                        print item.get_info()

                        print each_data[1].get_text().strip(), each_data[1].get_text().strip()
                        if item.type == "http" or item.type == "https":
                            self.ip_items.append(item)

            except Exception,e:
                print e

        url_xici = 'http://www.xicidaili.com/nn/{pid}'
        for i in range(1, self.count+1):
            url = url_xici.format(pid=i)
            parse_one_page(url)

            self._page_wait(i)


        print 'xicidaili success: {} have get {} items'.format('\n', len(self.ip_items))

    # 有代理
    def parse_youdaili(self):

        def parse_one_page(url):
            try:
                r = requests.get(url, headers=self.headers, timeout=10)
                soup = BeautifulSoup(r.text, "html5lib")
                print soup.get_text()
                body_data = soup.find('table', attrs={'id':'ip_list'})
                res_list = body_data.find_all('tr')
                for res in res_list:
                    each_data = res.find_all('td')
                    if len(each_data) > 6 and '.' in each_data[2].get_text():

                        item = IPItem()
                        item.ip = each_data[2].get_text().strip()
                        item.port = each_data[3].get_text().strip()
                        item.addr = each_data[4].get_text().strip()
                        item.type = each_data[6].get_text().strip().lower()
                        item.anonymous = each_data[5].get_text().strip()
                        print item.get_info()

                        print each_data[1].get_text().strip(), each_data[1].get_text().strip()
                        if item.type == "http" or item.type == "https":
                            self.ip_items.append(item)

            except Exception,e:
                print e

        def get_urls(url_origin):

            urls = []

            try:
                r = requests.get(url_origin, header=self.headers)
                soup = BeautifulSoup(r.text, "html5lib")
                ulNewsList= soup.find('ul', {'class':'newslist_line'})
                if ulNewsList:
                    liAll = ulNewsList.find_all('li')
                    for li in liAll:
                        try:
                            data_a = li.find('a')
                            href = data_a['href']
                            urls.append(href)
                        except Exception,e:
                            print e
            except Exception,e:
                print e

            return urls


        url_youdaili_origin = 'http://www.youdaili.net/Daili/guonei/'
        urls = get_urls(url_youdaili_origin)

        #ips = re.findall('\d+.\d+.\d+:\d+@HTTPS', r.text)

        for i in range(1, self.count+1):
            #url = url_xici.format(pid=i)
            #parse_one_page(url)

            self._page_wait(i)


        print 'youdaili success: {} have get {} items'.format('\n', len(self.ip_items))

    # 66ip代理
    def parse_66ip(self):
        url_xici = 'http://www.66ip.cn/areaindex_1/1.html'


    def _page_wait(self, now_page):
        if (now_page < self.count):
                print 'next page:', now_page+1
                time.sleep(self.wait_time)
        else:
            print 'parse finish'


    @fn_timer_
    def test_ip_speed(self):

        #多线程
        pool = ThreadPool(processes=20)
        pool.map(self.ping_one_ip, range(len(self.ip_items)))
        pool.close()
        pool.join()

        #单线程
        # for index in range(len(self.ip_items)):
        #     self.ping_one_ip(index)
        # t2 = time.time()
        # print "Total time running multi: %s seconds" % ( str(t1-t0))
        # print "Total time running single: %s seconds" % ( str(t2-t1))

        print len(self.ip_items)
        self.ip_items = [item for item in self.ip_items if item.speed >=0 and item.speed < 1500.0]    # 超时1.5s以内
        print len(self.ip_items)

        # s = requests.Session()
        #
        # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36'}
        #
        #
        # tmpItems = []
        # for item in self.ip_items:
        #
        #     http = str(item.type).lower()
        #     ip_proxy = "%s://%s:%s" % (http, item.ip, item.port)
        #     proxies = {http:ip_proxy}
        #     print proxies
        #     try:
        #
        #         r = requests.get("http://www.baidu.com", proxies=proxies, headers=headers, timeout=10)
        #         print r.status_code
        #         tmpItems.append(item)
        #         print ip_proxy, 'Good'
        #     except:
        #         print ip_proxy, 'timeout!'
        # self.ip_items = tmpItems



    def ping_one_ip(self, index):
        systemName = platform.system()
        if systemName == 'Windows':
            #p = Popen(["ping.exe",item.ip], stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
            p = Popen("ping.exe %s -n 1" % (self.ip_items[index].ip), stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
            out = p.stdout.read().decode('gbk').encode('utf8')

            m = re.search(u'=(\d+)ms', out)
            if m:
                s_r = self.ip_items[index].ip + ' time=' + m.group(1) + 'ms'
                print s_r
                self.ip_items[index].speed = float(m.group(1))
            else:
                s_r = self.ip_items[index].ip + ' time out'
                print s_r

        else:
            (command_output, exitstatus) = pexpect.run("ping -c1 %s" % self.ip_items[index].ip, timeout=5, withexitstatus=1)
            if exitstatus == 0:
                print command_output
                m = re.search("time=([\d\.]+)", command_output)
                if m:
                    s_r = self.ip_items[index].ip + ' time=' + m.group(1) + 'ms'
                    print s_r
                    self.ip_items[index].speed = float(m.group(1))
                else:
                    s_r = self.ip_items[index].ip + ' time out'
                    print s_r

    def save_data(self):
        df = DataFrame({'IP':[item.ip for item in self.ip_items],
                        'Port':[item.port for item in self.ip_items],
                       # 'Addr':[item.addr for item in self.ip_items],
                        'Type':[item.type for item in self.ip_items],
                        'Speed':[item.speed for item in self.ip_items]
                        }, columns=['IP', 'Port', 'Type', 'Speed'])

        df['Time'] = GetNowTime()

        #df = df.applymap(lambda x : encode_wrap(x))
        print df[:10]
        df = df.sort_index(by='Speed')

        #file_name = self.dir_path +'ip_proxy_' + GetNowDate()
        #df.to_csv(file_name + '.csv')
        #df.to_excel( 'ip.xlsx', index=False)

        df.to_sql(mysql_table_ip, engine, if_exists='append', index=False)

    @fn_timer_
    def run(self):

        self.parse()
        print 'test speed begin...'
        self.test_ip_speed()
        print 'test speed end'

        self.save_data()

class IPItem:
    def __init__(self):
        self.ip = ''    # IP
        self.port = ''  # Port
        self.addr = ''  # 位置
        self.type = ''  # 类型:http, https
        self.anonymous = '' # 匿名度
        self.speed = -1 #速度
    def get_info(self):
        return '{}://{}:{}  {}'.format(self.type, self.ip, self.port, self.addr)

if __name__ == "__main__":
    spider = IP_Proxy_Spider()
    spider.run()

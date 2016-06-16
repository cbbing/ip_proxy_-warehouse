#coding:utf-8

from selenium import webdriver
from bs4 import BeautifulSoup as bs

def get_ip_proxy(count=1000):
    dr = webdriver.PhantomJS()
    dr.get('http://www.daili666.net/web')
    tid = '**'
    dr.find_element_by_xpath('//input[@type="text" and @name="tid"]').send_keys(tid)
    dr.find_element_by_xpath('//input[@type="text" and @name="num"]').send_keys('0')

    dr.find_element_by_xpath('//input[@type="radio" and @name="foreign" and @value="none"]').click()
    dr.find_element_by_xpath('//input[@type="radio" and @name="download" and @value="true"]').click()
    dr.find_element_by_xpath('//input[@type="submit"]').click()

    soup = bs(dr.page_source, 'lxml')
    data = soup.find('body').text
    print data
    dr.quit()

get_ip_proxy()



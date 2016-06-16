# -*- coding:utf8 -*-

from ip_proxy_spider import IP_Proxy_Spider

def run_auto():
    ip_proxy = IP_Proxy_Spider()
    ip_proxy.run_add()
    ip_proxy.check_useful_in_db()

if __name__ == '__main__':
    run_auto()

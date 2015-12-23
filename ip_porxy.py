# -*- coding:utf8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import pandas as pd

from config import engine, mysql_table_ip

class IP_Proxy:

    def __init__(self):
        pass

    # 获取前100的IP代理地址
    def get_top_100_ip_proxy(self):
        sql = 'select * from {0} order by Speed limit 100'.format(mysql_table_ip)
        df = pd.read_sql_query(sql, engine)
        return df[['IP', 'Port', 'Type']].get_values()

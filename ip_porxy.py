# -*- coding:utf8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import pandas as pd

from config import engine, mysql_table_ip



# 获取IP代理地址
def get_ip_proxy(count=100):
    sql = 'select * from {0} order by Speed limit {1}'.format(mysql_table_ip, count)
    df = pd.read_sql_query(sql, engine)
    return df[['IP', 'Port', 'Type']].get_values()

if __name__ == '__main__':
    values = get_ip_proxy()
    print values[:10]
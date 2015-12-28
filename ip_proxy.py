# -*- coding:utf8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import pandas as pd

from sqlalchemy import create_engine

# mysql Host
host_mysql = 'rdsw5ilfm0dpf8lee609.mysql.rds.aliyuncs.com'
port_mysql = '3306'
user_mysql = 'licj_read'
pwd_mysql = '12356789'
db_name_mysql = 'wealth_db'

engine = create_engine('mysql+mysqldb://%s:%s@%s:%s/%s' % (user_mysql, pwd_mysql, host_mysql, port_mysql, db_name_mysql), connect_args={'charset':'utf8'})

mysql_table_ip = 'ip_proxy'

# 获取IP代理地址
def get_ip_proxy(count=100, result_in_DataFrame = False):
    sql = 'select IP, Port, Type from {0} where Speed > 0 order by Speed limit {1}'.format(mysql_table_ip, count)
    df = pd.read_sql_query(sql, engine)
    if result_in_DataFrame:
        return df
    else:
        return df[['IP', 'Port', 'Type']].get_values()

if __name__ == '__main__':
    values = get_ip_proxy()
    print values[:10]
#coding:utf-8
__author__ = 'cbb'

import platform, os, sys
from sqlalchemy import create_engine
from util.MyLogger import Logger

# mysql Host
host_mysql = 'rdsw5ilfm0dpf8lee609.mysql.rds.aliyuncs.com'
port_mysql = '3306'
user_mysql = 'licj'
pwd_mysql = 'AAaa1234'
db_name_mysql = 'wealth_db'

engine = create_engine('mysql+mysqldb://%s:%s@%s:%s/%s' % (user_mysql, pwd_mysql, host_mysql, port_mysql, db_name_mysql), connect_args={'charset':'utf8'})

mysql_table_ip = 'ip_proxy'
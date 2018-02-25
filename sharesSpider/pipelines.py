# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors
import time


class SharesspiderPipeline(object):

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        """1、@classmethod声明一个类方法，而对于平常我们见到的叫做实例方法。
           2、类方法的第一个参数cls（class的缩写，指这个类本身），而实例方法的第一个参数是self，表示该类的一个实例
           3、可以通过类来调用，就像C.f()，相当于java中的静态方法"""

        # 读取settings中配置的数据库参数
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=False
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)  # **表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        return cls(dbpool)  # # 相当于dbpool付给了这个类，self中可以得到

    def process_item(self, item, spider):
        res = self.dbpool.runInteraction(self.insert, item)
        return item

    def insert(self, conn, item):
        check_repeat_sql = 'select * from tb_shares where shares_num=%s' % item['shares_num']  # 查重
        conn.execute(check_repeat_sql)
        result = conn.fetchone()  # 返回的是一个dict对象

        if result is None or len(result) == 0:
            sql = 'insert into tb_shares (id, shares_num, shares_name, shares_href, create_time) values(%s, %s, %s, %s, %s)'
            param = (item['id'], item['shares_num'], item['shares_name'], item['shares_href'], item['create_time'])
            db_shares_id = item['id']
            conn.execute(sql, param)
        else:
            db_shares_id = result['id'].decode('utf-8')

        # 插入明细数据,也要判断时间是否重复
        check_repeat_sql = "select id from tb_shares_detailed where shares_id=%s and create_time=%s" % ('\'' + db_shares_id + '\'', '\'' + time.strftime("%Y-%m-%d", time.localtime()) + '\'')
        conn.execute(check_repeat_sql)
        result = conn.fetchone()  # 返回的是一个dict对象

        if result is None or len(result) == 0:
            sql = "insert into tb_shares_detailed(id, shares_id, create_time, open_price, close_price, ceilling_price, floor_price, rise_and_fall_range, rise_and_fall_quota, volume, turn_volume, turnover_rate, amplitude, p_e_ratio, state) " \
                  "values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

            param = (item['detailed_id'],
                     item['shares_id'],
                     item['create_time'],
                     item['open_price'],
                     item['close_price'],
                     item['ceilling_price'],
                     item['floor_price'],
                     item['rise_and_fall_range'],
                     item['rise_and_fall_quota'],
                     item['volume'],
                     item['turn_volume'],
                     item['turnover_rate'],
                     item['amplitude'],
                     item['p_e_ratio'],
                     item['state'])

            conn.execute(sql, param)


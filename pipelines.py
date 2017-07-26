# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors

class JingyuPipeline(object):
    def process_item(self, item, spider):
        return item

class JingyuImgPathPipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if 'Cover_img_url' in item:
            for ok,value in results:
                Cover_img_path = value['path']

            item['Cover_img_path']=Cover_img_path
        return item

class MysqlPipeline(object):
    #采用同步的机制写入mysql
    def __init__(self):
        self.conn = MySQLdb.connect('localhost', 'root', '0000', 'jingyu_book', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
                    insert into Jingyu_bookinfo(Title,Author,Url,Tags,Fav_nums,Pop_nums,Score,Cover_img_url,Cover_img_path)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
        self.cursor.execute(insert_sql, (item['Title'], item['Author'], item['Url'], item['Tags'],
                        item['Fav_nums'],item['Pop_nums'],item['Score'],item['Cover_img_url'][0],item['Cover_img_path']))
        self.conn.commit()

class MysqlTwistedPipline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host = settings["MYSQL_HOST"],
            db = settings["MYSQL_DBNAME"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        #使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider) #处理异常

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print (failure)

    def do_insert(self, cursor, item):
        #执行具体的插入
        #根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql = """
            insert into Jingyu_bookinfo(Title,Author,Url,Tags,Fav_nums,Pop_nums,Score,Cover_img_url,Cover_img_path)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_sql,
                       (item['Title'], item['Author'], item['Url'], item['Tags'],
                        item['Fav_nums'],item['Pop_nums'],item['Score'],item['Cover_img_url'],item['Cover_img_path']))
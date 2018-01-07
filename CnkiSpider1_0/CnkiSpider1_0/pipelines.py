# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3

class Cnkispider10Pipeline(object):
    def open_spider(self, spider):
        self.con = sqlite3.connect("cnki.sqlite")#链接数据库
        self.cu = self.con.cursor()
    def process_item(self, item, spider):
        print(spider.name,'pipelines')
        insert_sql = "insert into cnki (title, time, source, institution, refer, keywords, abstract, download) values('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(item['title'],
                                                                                                                                               item['time'],
                                                                                                                                               item['source'],
                                                                                                                                               item['institution'],
                                                                                                                                               item['refer'],
                                                                                                                                               item['keywords'],
                                                                                                                                               item['abstract'],
                                                                                                                                               item['download'],
                                                                                                                                               )
        print(insert_sql)
        self.cu.execute(insert_sql)
        self.con.commit()
        return item
    def spider_close(self, spider):
        self.con.close()
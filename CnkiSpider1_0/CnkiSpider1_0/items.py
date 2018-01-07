# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Cnkispider10Item(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    time = scrapy.Field()
    source = scrapy.Field()
    institution = scrapy.Field()
    refer = scrapy.Field()
    
    keywords = scrapy.Field()
    abstract = scrapy.Field()
    download = scrapy.Field()
    pass

# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst,MapCompose


class JingyuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

# class

class JingYuBookLoader(ItemLoader):
    default_input_processor = TakeFirst()

def strip(value):
    _value = value.strip()
    return _value

def re(value):
    return value

class JingYuBookItem(scrapy.Item):
    Title= scrapy.Field()
    Author= scrapy.Field()
    Url = scrapy.Field()
    Tags= scrapy.Field()
    Fav_nums= scrapy.Field()
    Pop_nums= scrapy.Field()
    Score= scrapy.Field()
    Cover_img_url= scrapy.Field()
    Cover_img_url_forSQL = scrapy.Field()
    Cover_img_path= scrapy.Field()


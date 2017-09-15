# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Money2020Item(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    title = scrapy.Field()
    company = scrapy.Field()
    bio = scrapy.Field()
    session = scrapy.Field()
    url = scrapy.Field()
    

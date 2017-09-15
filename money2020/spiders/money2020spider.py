# -*- coding: utf-8 -*-
import scrapy


class Money2020spiderSpider(scrapy.Spider):
    name = 'money2020spider'
    allowed_domains = ['us.money2020.com']
    start_urls = ['http://us.money2020.com/']

    def parse(self, response):
        pass

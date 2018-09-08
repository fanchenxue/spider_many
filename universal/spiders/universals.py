# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join, Compose, Identity



class UniversalsSpider(CrawlSpider):
    # name = 'universals'
    # allowed_domains = get_config.get('allowed_domains')
    # start_urls = get_config.get('start_urls')


    def parse_item(self, response):
        i = {}
        return i
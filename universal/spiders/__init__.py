# -*- coding: utf-8 -*-
# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

from scrapy.spiders import CrawlSpider
from universal.Get_configs import get_config
from universal.rules import rules
from scrapy.loader import ItemLoader
from scrapy.loader.processors import  Join, Compose, Identity
from universal.items import UniversalItem
from universal import urls

#init使用模块rules与get_congifs获取所有的初始配置,文件是json文件
class UniversalsSpider(CrawlSpider):
    name = 'universals'
    def __init__(self, name, *args, **kwargs):
        #引入读取json文件,获取所有配置
        config = get_config(name)
        self.config = config
        #获取rules爬去规则
        self.rules = rules.get(config.get('rules'))
        #从json文件内 获取爬去网站链接
        start_urls = config.get('start_urls')
        if start_urls.get('type') == 'static':
            self.start_urls = start_urls.get('value')
        elif start_urls.get('type') == 'dynamic':
            self.start_urls = list(eval('urls.' + start_urls.get('method'))(*start_urls.get('args', [])))
        self.allowed_domains = config.get('allowed_domains')
        super(UniversalsSpider, self).__init__(*args, **kwargs)
    def parse_item(self, response):
        item = self.config.get('item')
        if item:
            #引入模块from universal.items import UniversalItem,
            cls = eval(item.get('class'))()
            #同等于ChinaLoader(item=ZhonghuakejiItem(), response=response),eval(item.get('loader'))等于ChinaLoader
            #利用eval反转出对象类型
            loader = eval(item.get('loader'))(cls, response=response)
            #动态获取属性
            for key, value in item.get('attrs').items():
                for extractor in value:
                    if extractor.get('method') == 'xpath':
                        loader.add_xpath(key, *extractor.get('args'), **{'re': extractor.get('re')})
                    if extractor.get('method') == 'css':
                        loader.add_css(key, *extractor.get('args'), **{'re': extractor.get('re')})
                    if extractor.get('method') == 'value':
                        loader.add_value(key, *extractor.get('args'), **{'re': extractor.get('re')})
                    if extractor.get('method') == 'attr':
                        loader.add_value(key, getattr(response, *extractor.get('args')))
            yield loader.load_item()


class NewsLoader(ItemLoader):
    default_input_processor = Identity()
class ChinaLoader(NewsLoader):
    text_out = Compose(Join(), lambda s: s.strip().replace('\r\n', ''))
    source_out = Compose(Join(), lambda s: s.strip())
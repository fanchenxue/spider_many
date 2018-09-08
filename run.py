# -*- coding: utf-8 -*-
import sys
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from universal.Get_configs import get_config
from universal.spiders.universals import UniversalsSpider

def runspider():
    name = sys.argv[1]
    custom_settings = get_config(name)
    #爬去使用的爬虫名称
    spider = custom_settings.get('spider', custom_settings.get('spider'))
    project_settings = get_project_settings()
    settings = dict(project_settings.copy())
    #合并配置
    settings.update(custom_settings.get('settings'))
    process = CrawlerProcess(settings)
    #启动爬虫
    process.crawl(spider, **{'name': name})
    process.start()
if __name__ == '__main__':
    runspider()
# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

class ChinahrSpider(CrawlSpider):
    name = "chinahr"

    start_urls=[
        'http://www.chinahr.com/beijing'
    ]
    rules = (
        Rule(LinkExtractor(allow=('www.chinahr.com/job/[0-9a-z]*\.html',)), callback='parse_one_job', follow=True),
        Rule(LinkExtractor(allow=('www.chinahr.com/job/[0-9a-z]*\.html',)), callback='parse_one_job', follow=True),
        Rule(LinkExtractor(allow=('www.chinahr.com',), deny=('php$', 'php?',
                                                             )), follow=True),
    )

    def parse_one_jop(self,response):

        def do_item(item):
            if item and isinstance(item,list):
                return item[0]
            return item
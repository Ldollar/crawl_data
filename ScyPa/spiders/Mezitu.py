# -*- coding: utf-8 -*-
import logging

from scrapy import Selector
from scrapy import selector
from scrapy.exporters import JsonLinesItemExporter
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor


from ScyPa.items import MeiTu


class MeiZitu(CrawlSpider):
    name = "meizitu1"
    #allowed_domains="jandan.net"
    start_urls = [
        "http://jandan.net/ooxx/page-1#comments"
    ]
    try:
        rules = (
            Rule(LinkExtractor( tags=('img'), attrs=('src',), unique=True), callback="parse_imageUrl",follow=True
                 ),
            Rule(LinkExtractor(allow="ooxx/page-/d+#comments",tags=('a'),attrs=('href',),unique=True),callback="parse_click")
        )
    except Exception,e:
        print e

    for i in xrange(1,500):
        start_urls.append("http://jandan.net/ooxx/page-"+str(i)+"#comments")

    def parse(self, response):
        self.log("hi", level=logging.DEBUG)

        item = MeiTu()
        itemurl = []
        list=Selector(response=response).xpath("//div[@class='text']").css("img::attr(src)").extract()
        for i in list:
            url="http:"+str(i)
            itemurl.append(url)
        item["image_urls"] = itemurl#Selector(response=response).xpath("//div[contains(@class,'text')]").css("img::attr(src)").extract()

        return item

        #JsonLinesItemExporter(file="F:\PYTHON_PROJIECT\spiderProject\ScyPa\ScyPa\\1.json")



        #driver=webdriver.ActionChains



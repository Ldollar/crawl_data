# -*- coding: utf-8 -*-
import logging

import copy
from scrapy import Request, item
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from ScyPa.items import Dingdian


class DingdianNovel_spider(CrawlSpider):
    item = Dingdian()
    name = "novel_dingdian"
    #allowed_domains = ""
    start_urls = [
        "http://www.23us.com/quanben/1"
    ]

    rules = (
        Rule(LinkExtractor(allow="http://www.23us.com/html/\d+/\d+/",deny=".*?.html",unique=True),callback="chapter_parse",
             follow=True,),
        #Rule(LinkExtractor(allow="\d+.html",process_value=None  ), callback="contents_parse",
             #follow=True,process_links=),
        Rule(LinkExtractor(allow="http://www.23us.com/class/\S+.html", process_value=None,unique=True), callback="title_parse",
             follow=True,)
            )




    def title_parse(self,response):
        item = Dingdian()
        #response.metal = item
        titles =  response.css("tr td.L").xpath(".//a[2]/text()").extract()
        for title1 in enumerate(titles):
            item["title"] = title1



    def chapter_parse(self,response):
        #l = ItemLoader(item=Dingdian(), response=response)
        #l.add_css('chapter',"table[id*='at'] tr td.L a::text")
        item = Dingdian()
        chapters = response.css("table[id*='at'] tr td.L a::text").extract()
        next_url = response.css("table[id*='at'] tr td.L a::attr(href)").extract()
        for chapter1 in enumerate(chapters):

            item["chapter"] = chapter1
            #print chapter1
        for url in enumerate(next_url):
            self.log(message=response.url+url+"--------", level=logging.DEBUG)
            yield Request(response.url+url,callback=self.contents_parse,meta={"item":copy.deepcopy(item)},dont_filter=True)




        # response.css("table[id*='at'] tr td.L a::text").extract()  各章节的名字
        # response.css("table[id*='at'] tr td.L a::attr(href)").extract() 各章节详细地址


    def contents_parse(self, response):
        item=response.meta
        response.replace(body=response.body.replace(b'<br>', b'\n'))
        contentss=response.css("dd[id*='tent']::text").extract()  #获取文章内容
        item["contents"] = contentss
        self.log(message="---------------contents-----------------", level=logging.DEBUG)
        yield item








# response.css("tr td.L").xpath(".//a[2]/text()").extract() 找到文章名字
# response.css("tr td.L").xpath(".//a[2]/@href").extract()  文章链接
# response.css("div[id*='link'] a[class='next']::attr(href)").extract()  下一页的地址
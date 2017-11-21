# -*- coding: utf-8 -*-
import logging

import sys

import copy
from scrapy import Request, selector
from scrapy import Selector, item
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from ScyPa import items
from ScyPa.items import Dingdian, Chapters


class EasouNovel(CrawlSpider):
    name = "easounovel"
    allowed_domains = "easou.com"
    start_urls = [
        "http://book.easou.com/w/booklib/all_c_l_2_0_1.html"
    ]

    rules = (
        Rule(LinkExtractor(allow="booklib/(\S+).html", tags=("a"), attrs=("href"),
                           restrict_xpaths="//div[@class=wrap/a]"), callback="parse_next"),
        #Rule(LinkExtractor(allow="/w/searchNovel/\S+.html", tags=("a"), attrs=("href",)), callback="novel_detail_parse",
             #follow=True)
    )

    def parse(self, response):
        # response.xpath("//ul/li/span[@class='name']/a/text()").extract()[0]
        item = Dingdian()

        self.log('1231231', level=logging.DEBUG)

        titles = response.xpath("//div [@class='listcontent']/ul/li")
        to_novel_url = response.xpath("//div [@class='listcontent']/ul/li/span[@class='name']/a/@href").extract()   #进入小说，包含同名
        #for t in titles:
            #item["title"] = t.xpath(".//span[@class='name']/a/text()").extract_first()
            # item["page"] = t.xpath("div[2]/div[1]/div[2]/div[3]/div/span[2]")
            #item["category"] = t.xpath(".//span[@class='kind']/a/text()").extract_first()
            #item["state"] = t.xpath(".//span[@class='state']/span/text()").extract_first()
            #item["lastdate"] = t.xpath(".//span[@class='date']/text()").extract_first()
            #yield item
            # nexts =response.xpath("//html/body/div[2]/div[1]/div[2]/div[3]/div/a[last()]/span/text()").extract()

        next_url = response.xpath("/html/body/div[2]/div[1]/div[2]/div[3]/div/a[last()]/@href").extract_first()
        self.log(message=next_url, level=logging.DEBUG)

        if next_url and response.xpath(
                "/html/body/div[2]/div[1]/div[2]/div[3]/div/a[last()]/span/text()").extract_first() == u"下一页":
            url = "http://book.easou.com" + next_url
            yield Request(url, callback=self.parse, dont_filter=True)
            # return item
        if to_novel_url:
            for n in to_novel_url:
                url_name1 = "http://book.easou.com" + n
                yield Request(url=url_name1, callback=self.to_detail_parse,dont_filter=True)

    def to_detail_parse(self, response):
        url_to_novel = response.xpath("/html/body/div[2]/div[1]/div[3]/div/ul/li[1]/div[2]/div[1]/a/@href").extract_first()
        if url_to_novel:
            url_to_novel1="http://book.easou.com"+url_to_novel
            yield Request(url_to_novel1, callback=self.to_novel_detail_parse,dont_filter=True)

    def to_novel_detail_parse(self, response):


        detail_url = response.xpath(
            "/html/body/div[@class='content']/div[@class='left']/div[@class='category']/div[@class='allcategore']/span/a/@href").extract_first()
        if detail_url:
            detail_url1="http://book.easou.com"+ detail_url
            yield Request(detail_url1,callback=self.novel_detail_parse,dont_filter=True)
    def novel_detail_parse(self, response):
        item = Chapters()

        self.log("-----------------------------------daowole",level=logging.DEBUG)
        title = response.xpath("/html/body/div[2]/div[1]/div[1]/div/div[1]/h1/text()").extract_first()
        category = response.xpath("/html/body/div[2]/div[1]/div[1]/div/div[2]/div[2]/span/a/text()").extract_first()
        item["title"] = title
        item["category"] = category
        chapters = response.xpath("//div[@class='left']/div[@class='category']/ul/li")
        for keys,j in enumerate(chapters):
            item["chapter"] = j.xpath(".//span/a[@class='common']/text()").extract_first()
            item["link"] = j.xpath(".//span/a[@class='common']/@href").extract_first()
            link =j.xpath(".//span/a[@class='common']/@href").extract_first()
        #yield item
            if link:
                url_content="http://book.easou.com"+link
                yield Request(url_content,callback=self.get_content_parse,dont_filter=True,meta={"item1":copy.deepcopy(item)})
                #'dont_redirect': True,
                 # 'handle_httpstatus_list': [301,302]})

    def get_content_parse(self,response):
        self.log("-----------------------------------contents", level=logging.DEBUG)
        item = response.meta["item1"]
        response.replace(body=response.body.replace(b'<br>', b'\n'))

        item["contents"] = response.xpath("//div[contains(@id,'ent') or contains(@class,'ent') or contains(@id,'ext') or contains(@class,'txt')][/*]/text()| //div[contains(@id,'ent') or contains(@class,'ent') or contains(@id,'ext') or contains(@class,'txt')]/*/text()").extract()
        #if item["contents"] is None:
            #item["contents"] = response.xpath(
                #"//div[contains(@id,'ent') or contains(@class,'ent') or contains(@id,'ext')]/*/text()").extract()

        yield item


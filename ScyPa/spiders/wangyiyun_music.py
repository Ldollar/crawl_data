# -*- coding: utf-8 -*-
from fpformat import extract

from scrapy import Spider
from scrapy.spiders import CrawlSpider
from selenium import webdriver
from selenium.webdriver.common import utils

from ScyPa.items import WangyiYunItem


class WangyiYunMusic(CrawlSpider):
    name = 'wangyiyun'
    allowed_domains = ['music.163.com']
    start_urls = [
        'http://music.163.com'
    ]

    def parse(self, response):
        item = WangyiYunItem()
        driver = webdriver.PhantomJS(
            executable_path="F:\pythonEnv\ENV\Scripts\phantomjs-2.1.1-windows\phantomjs-2.1.1-windows\\bin\phantomjs.exe")
        driver.get(response.url)
        driver.switch_to.frame('g_iframe')
        s = driver.find_elements_by_xpath("//ul/li/div[@class='u-cover u-cover-1']/a[@class='msk']")
        for i in s :
            item["name"] = i.get_attribute("title")
            yield item
        driver.switch_to.default_content()
        driver.find_element_by_link_text(u"歌手").click()

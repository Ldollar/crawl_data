# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import os
import shutil

import scrapy
import sys
from scrapy import Request
from scrapy import spiders, item
from scrapy.exceptions import DropItem
from scrapy.pipelines.files import FilesPipeline
from scrapy.pipelines.images import ImagesPipeline

from ScyPa.items import MeiTu, Chapters

reload(sys)
sys.setdefaultencoding("utf-8")


class ScypaPipeline(object):
    def process_item(self, item, spider):
        return item


class MyImagesPipeline(ImagesPipeline):
    if isinstance(item, MeiTu):  # 判断item来自哪里

        def get_media_requests(self, item, info):
            for image_url in item['image_urls']:
                try:
                    yield scrapy.Request(image_url)
                except Exception, e:
                    print e

        def item_completed(self, results, item, info):
            return super(MyImagesPipeline, self).item_completed(results, item, info)


class NullPipeline(object):
    #if isinstance(item, Chapters):
    def process_item(self, item, spider):
        if isinstance(item, Chapters):

            logging.log(msg="++++++++++++++++++++++++0", level=logging.DEBUG)
            if item["title"]:

                if item["contents"] is None and item["chapter"] is None:
                    raise DropItem(repr(item))
                    # if item["title"] != None and item["link"] != None:
                #else:
                    #item["title"] = item["title"]
                    #item["link"] = item["link"]
                    #item["chapter"] = item["chapter"]
                    #item["category"] = item["category"]
                    #item["contents"] = item["contents"]

                    # r=os.path.join("./"+item["category"],item["title"])


            logging.log(msg="------writing the file------------", level=logging.DEBUG)
            path = ".\\" + item["category"] + r"\\" + item["title"]
            if not os.path.exists(path):
                os.makedirs(path)

            if os.path.exists(path):
                if not os.path.exists(".\\" + item["category"] + "\\" + item["title"] + "\\" + item["chapter"] + ".txt") :
                    if item["contents"] :
                        if not os.path.exists(".\\" + item["category"] + "\\" + item["title"] + "\\" + item["chapter"] + ".txt"):
                            with open(".\\" + item["category"] + "\\" + item["title"] + "\\" + item["chapter"] + ".txt",'ab+') as f:

                                #f.write(item["contents"])
                                for i in item["contents"]:
                                    "".join(i.split())
                                    f.write(i + "\n")
                            logging.log(msg="-----------write down ------------", level=logging.DEBUG)
            else:
                logging.log(msg="------writing ??????????????????------------", level=logging.DEBUG)

                #else:
                    #pass






                        # return item
                        # else:
                        # raise DropItem("Missing chapter in %s" % item)


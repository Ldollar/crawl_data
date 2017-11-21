# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MeiTu(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 以下定义自己所需要的数据模型，类似于字典key-value
    image_urls = scrapy.Field()
    images = scrapy.Field()


class Dingdian(scrapy.Item):
    chapter = scrapy.Field()
    link = scrapy.Field()
    title = scrapy.Field()
    category = scrapy.Field()
    contents = scrapy.Field()

class Chapters (scrapy.Item):
    chapter = scrapy.Field()
    link = scrapy.Field()
    title = scrapy.Field()
    category = scrapy.Field()
    contents = scrapy.Field()


class PixivCrawlItem(scrapy.Item):
    title = scrapy.Field()
    date = scrapy.Field()
    img_urls = scrapy.Field()
    user_id = scrapy.Field()
    user_name = scrapy.Field()
    rank = scrapy.Field()
    yes_rank = scrapy.Field()
    total_score = scrapy.Field()
    views = scrapy.Field()
    is_sexual = scrapy.Field()
    illust_id = scrapy.Field()
    tags = scrapy.Field()
    url = scrapy.Field()
    image_paths = scrapy.Field()

class DoubanMovieItem(scrapy.Item):
    # 排名
    ranking = scrapy.Field()
    # 电影名称
    movie_name = scrapy.Field()
    # 评分
    score = scrapy.Field()
    # 评论人数
    score_num = scrapy.Field()

class WangyiYunItem(scrapy.Item):

    name = scrapy.Field()
    range = scrapy.Field()
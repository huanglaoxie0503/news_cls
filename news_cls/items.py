# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from tools.es_models import NewsClsType


class NewsClsItem(scrapy.Item):
    """
    财联社新闻Item
    """
    article_id = scrapy.Field()
    title = scrapy.Field()
    brief = scrapy.Field()
    content = scrapy.Field()
    create_date = scrapy.Field()
    stock_code = scrapy.Field()
    stock_name = scrapy.Field()
    share_url = scrapy.Field()

    def save_to_es(self):
        # 将 item 转换位 es 数据
        article = NewsClsType()
        article.article_id = self['article_id']
        article.title = self['title']
        article.brief = self['brief']
        article.content = self['content']
        article.create_date = self['create_date']
        article.stock_code = self['stock_code']
        article.stock_name = self['stock_name']
        article.share_url = self['share_url']

        article.save()

        return


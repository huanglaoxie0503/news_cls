# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from tools.es_models import NewsClsType
from elasticsearch_dsl.connections import connections

es = connections.create_connection(NewsClsType._doc_type.using)


def gen_suggest(index, info_tuple):
    # 根据字符串生成搜索建议字符串数组
    user_words = set()
    suggests = []
    for text, weight in info_tuple:
        if text:
            # 调用 es 的 Analyzer 接口分析字符串
            words = es.indices.analyze(index=index, analyzer="ik_max_word", params={'filter': ["lowercase"]}, body=text)
            # analyzed_words = set([r["token"] for r in words if len(r["token"]) > 1])
            analyzed_words = set([r["token"] for r in words["tokens"] if len(r["token"]) > 1])
            new_words = analyzed_words - user_words
        else:
            new_words = set()

        if new_words:
            suggests.append({"input": list(new_words), "weight": weight})
    return suggests


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
    url = scrapy.Field()
    source = scrapy.Field()
    website = scrapy.Field()

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
        article.share_url = self['url']
        article.source = self['source']
        article.website = self['website']

        article.suggest = gen_suggest(NewsClsType._doc_type.index,
                                      ((article.title, 10), (article.brief, 7)))

        article.save()

        return

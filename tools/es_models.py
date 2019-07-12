# -*- coding: utf-8 -*-
from elasticsearch_dsl import DocType, Date, Nested, Boolean, analyzer, InnerObjectWrapper, Completion, Keyword, Text, Integer
from elasticsearch_dsl.connections import connections

connections.create_connection(hosts=["localhost"])


class NewsClsType(DocType):
    # 财联社新闻 构建 es 模型
    article_id = Integer()
    title = Text(analyzer="ik_max_word")
    brief = Text(analyzer="ik_max_word")
    content = Text(analyzer="ik_max_word")
    create_date = Date()
    url = Keyword()
    stock_code = Keyword()
    stock_name = Keyword()
    share_url = Keyword()

    class Meta:
        index = "news_cls"
        doc_type = "news"


if __name__ == '__main__':
    NewsClsType.init()

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ElasticSearchPipeline(object):
    """
    将数据写入到 ElasticSearch 中
    """
    def process_item(self, item, spider):
        item.save_to_es()

        return item

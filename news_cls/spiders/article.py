# -*- coding: utf-8 -*-
import scrapy
import json
import datetime
import time
from hashlib import sha1
from hashlib import md5

from news_cls.items import NewsClsItem


class ArticleSpider(scrapy.Spider):
    name = 'article'
    allowed_domains = ['www.cls.cn']
    start_urls = ['http://www.cls.cn/']
    dt = int(time.time())

    params = "app=CailianpressWeb&hasFirstVipArticle=1&last_time={0}&os=web&refresh_type=0&rn=20&subscribedColumnIds=&sv=6.8.0".format(dt)

    def start_requests(self):
        sign = self.get_sign(self.params)
        # 4c321210d34ada301e507ad42f5757a5
        url = 'https://www.cailianpress.com/nodeapi/telegraphs?refresh_type=1&rn=20&sign={0}'.format(sign)
        headers = {
            "Host": "www.cls.cn",
            "Referer": "https://www.cls.cn/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        }
        yield scrapy.Request(url, headers=headers)

    def parse(self, response):
        result = response.text
        json_data = json.loads(result)
        roll_data = json_data['data']['roll_data']
        for row in roll_data:
            article_id = row['id']
            title = row['title']
            brief = row['brief']
            content = row['content']
            share_url = row['shareurl']
            create_date = row['sort_score']
            stock_list = row['stock_list']
            if stock_list:
                stock_code = stock_list[0]['StockID']
                stock_name = stock_list[0]['name']
            else:
                stock_code = None
                stock_name = None

            if len(title) == 0:
                title = brief

            item = NewsClsItem()
            item['article_id'] = article_id
            item['title'] = title
            item['brief'] = brief
            item['content'] = content
            item['url'] = share_url
            item['create_date'] = self.time_switch(int(create_date))
            item['stock_code'] = stock_code
            item['stock_name'] = stock_name
            item['source'] = "财联社"
            item['website'] = "https://www.cls.cn"

            yield item

    def time_switch(self, time_stamp):
        date_array = datetime.datetime.utcfromtimestamp(time_stamp)
        other_style_time = date_array.strftime("%Y-%m-%d %H:%M:%S")
        return other_style_time

    def get_sign(self, keywords):
        # 首先sha1加密
        psw = sha1()
        psw.update(keywords.encode('utf8'))
        s_pwd_sha1 = psw.hexdigest()
        # sha1加密结果再次md5加密
        hash_md5 = md5(s_pwd_sha1.encode('utf8'))
        psw = hash_md5.hexdigest()
        return psw

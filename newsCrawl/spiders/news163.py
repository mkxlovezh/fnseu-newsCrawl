# -*- coding: utf-8 -*-
import scrapy
import json
import re
from scrapy.http import Request
from newsCrawl.config.config import all_rules
from newsCrawl.items import NewscrawlItem
from newsCrawl.extract.parsepage import *

class News163Spider(scrapy.Spider):
    name = 'news163'
    allowed_domains = ['news.163.com']
    start_urls = all_rules.start_urls['news163']

    def parse(self, response):
        jsonRegin = response.body.decode('gbk')
        jsons = json.loads(jsonRegin[9:len(jsonRegin) - 1])
        data = jsons['news']
        category=jsons['category']
        categorys={}
        for i in range(len(category)):
            categorys[i]=category[i]['n']

        for i in range(len(data)):
            for datai in data[i]:
                items = {}
                items['time']=datai['p']
                items['title']=datai['t']
                items['type']=categorys[datai['c']]
                yield Request(datai['l'],callback=self.parse_page,meta={'detail': items})

    def parse_page(self, response):
        item = NewscrawlItem()
        items = response.meta['detail']
        item['url'] = response.url
        item['title'] = items['title']
        item['time'] = items['time']
        item['source'] = extract_source(Selector(text=response.body.decode('gbk')))
        item['img_url'] = extract_img(Selector(text=response.body.decode('gbk')))
        item['content'] = extract_content(Selector(text=response.body.decode('gbk')))
        item['abstract'] = extract_abstract(Selector(text=response.body.decode('gbk')))
        item['type'] = items['type']

        return item


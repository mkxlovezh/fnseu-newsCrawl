# -*- coding: utf-8 -*-
import scrapy
import time
import json
from scrapy.http import Request
from newsCrawl.items import NewscrawlItem
from newsCrawl.extract.parsepage import *
from newsCrawl.config.config import all_rules
class PeopleSpider(scrapy.Spider):
    name = 'people'
    allowed_domains = ['people.com.cn']
    urls=[]
    urls.append((all_rules.start_urls['people'][0])+str(int(time.time())))
    start_urls=urls

    def parse(self, response):
        urls=[]
        jsons=json.loads(response.body)
        for it in jsons['items']:
            items = {}
            items['title']=it['title']
            items['time']=it['date']
            print()
            yield Request(it['url'],callback=self.parse_page,meta={'detail':items})
    def parse_page(self,response):
        item=NewscrawlItem()
        item['url'] = response.url
        items = response.meta['detail']
        item['title'] = items['title']
        item['time'] = items['time']
        item['source'] = extract_source(Selector(text=response.body.decode('gbk')))
        item['img_url'] = extract_img(Selector(text=response.body.decode('gbk')))
        item['content'] = extract_content(Selector(text=response.body.decode('gbk')))
        item['abstract'] = extract_abstract(Selector(text=response.body.decode('gbk')))
        item['type'] = extract_type(response.url, 'people')
        return item
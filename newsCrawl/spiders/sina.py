# -*- coding: utf-8 -*-
import scrapy
import re
import json
import time
from scrapy.selector import Selector
from newsCrawl.extract.parsepage import extract_abstract
from newsCrawl.extract.parsepage import extract_content
from newsCrawl.extract.parsepage import extract_type
from scrapy.http import Request
from newsCrawl.items import NewscrawlItem
from newsCrawl.config.config import all_rules
class SinaSpider(scrapy.Spider):
    name = 'sina'
    allowed_domains = ['sina.com.cn']
    start_urls = all_rules.start_urls['sina']
    def parse(self, response):
        jsonRegin=response.body.decode('utf-8')
        jsondata=re.findall("\(\{.*\}\)",jsonRegin)[0]
        jsons=json.loads(jsondata[1:len(jsondata)-1])
        data=jsons['result']['data']
        for i in range(len(data)):
            items = {}
            items['title']=data[i]['title']
            items['url']=data[i]['url']
            times=time.localtime((int)(data[i]['intime']))
            items['time']=time.strftime('%Y-%m-%d %H:%M:%S',times)
            items['source']=data[i]["media_name"]
            if len(data[i]['images'])>0:
                items['img_url']=data[i]['images'][0]['u']
            else:
                items['img_url']=""
            yield Request(items['url'],callback=self.parse_page,meta={'detail':items})
    def parse_page(self,response):
        item=NewscrawlItem()
        items=response.meta['detail']
        item['url'] = items['url']
        item['title'] = items['title']
        item['time'] = items['time']
        item['source']=items['source']
        item['img_url'] = items['img_url']
        item['content']=extract_content(Selector(text=response.body.decode('utf-8')))
        item['abstract']=extract_abstract(Selector(text=response.body.decode('utf-8')))
        item['type']=extract_type(response.url,'sina')
        return item




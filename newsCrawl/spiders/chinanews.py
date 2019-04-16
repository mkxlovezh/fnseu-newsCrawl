# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.selector import Selector
from scrapy.http import Request
from newsCrawl.items import NewscrawlItem
from newsCrawl.extract.parsepage import *
from newsCrawl.config.config import all_rules

class ChinanewsSpider(scrapy.Spider):
    name = 'chinanews'
    allowed_domains = ['chinanews.com']
    start_urls = all_rules.start_urls['chinanews']

    def parse(self, response):
        urls = Selector(response).xpath('//div[@id="content_right"]/div[@class="content_list"]/ul//li/div[2]/a[1]/@href').extract()
        urls_real=[]
        for url in urls:
            yield Request(response.urljoin(url),callback=self.parse_page)
    def parse_page(self,response):
        item=NewscrawlItem()
        item['url'] = response.url
        item['title'] = extract_title(Selector(text=response.body.decode('gbk')))
        item['time'] = extract_time(Selector(text=response.body.decode('gbk')))
        item['source'] = extract_source(Selector(text=response.body.decode('gbk')))
        item['img_url'] = extract_img(Selector(text=response.body.decode('gbk')))
        item['content'] = extract_content(Selector(text=response.body.decode('gbk')))
        item['abstract'] = extract_abstract(Selector(text=response.body.decode('gbk')))
        item['type'] = extract_type(response.url, 'chinanews')
        return item


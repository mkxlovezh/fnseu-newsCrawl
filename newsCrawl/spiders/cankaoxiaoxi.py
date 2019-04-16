# -*- coding: utf-8 -*-
import scrapy
from newsCrawl.config.config import all_rules
from scrapy.selector import Selector
from scrapy.http.request import Request
from newsCrawl.items import NewscrawlItem
from newsCrawl.extract.parsepage import extract_abstract
from newsCrawl.extract.parsepage import extract_source
from newsCrawl.extract.parsepage import extract_content
from newsCrawl.extract.parsepage import extract_img
from newsCrawl.extract.parsepage import extract_type
from newsCrawl.extract.parsepage import extract_time
from newsCrawl.extract.parsepage import extract_title
from newsCrawl.logs.logtools import write_info
from newsCrawl.logs.logtools import write_sys
class CankaoxiaoxiSpider(scrapy.Spider):
    name = 'cankaoxiaoxi'
    allowed_domains = ['cankaoxiaoxi.com']
    start_urls = all_rules.start_urls['cankaoxiaoxi']

    def parse(self, response):
        times=Selector(response).xpath("//ul[@class='txt-list-a fz-14 clear']//li/span/text()").extract()
        titles=Selector(response).xpath("//ul[@class='txt-list-a fz-14 clear']//li/a/text()").extract()
        urls=Selector(response).xpath("//ul[@class='txt-list-a fz-14 clear']//li/a/@href").extract()
        for i in range(len(urls)):
            items = {}
            items['title'] = titles[i]
            items['time'] = times[i]
            yield Request(url=urls[i],callback=self.parse_page,meta={'detail':items})
    def parse_page(self,response):
        item = NewscrawlItem()
        item['url']=response.url
        items=response.meta['detail']
        item['title']=items['title']
        item['time']=items['time']
        item['abstract']=extract_abstract(Selector(text=response.body.decode('UTF-8')))
        item['source']=extract_source(Selector(text=response.body.decode("UTF-8")))
        item['content']=extract_content(Selector(text=response.body.decode("UTF-8")))
        item['img_url'] = extract_img(Selector(text=response.body.decode("UTF-8")))
        item['type'] = extract_type(response.url,"cankaoxiaoxi")
        next_page=Selector(text=response.body.decode("UTF-8")).xpath("//div[@class='page']/ul//li/a[@id='next_page']/@href").extract()
        if len(next_page)>0:

            yield Request(url=next_page[0],callback=self.relate_page)
        else:
            write_sys(item['title'])
            yield item

    def relate_page(self,response):
        if response.url!="http://www.cankaoxiaoxi.com/":
            item = NewscrawlItem()
            item['url']=response.url
            item['title']=extract_title(Selector(text=response.body.decode('UTF-8')))
            item['time']=extract_time(Selector(text=response.body.decode('UTF-8')))
            item['abstract']=extract_abstract(Selector(text=response.body.decode('UTF-8')))
            item['source']=extract_source(Selector(text=response.body.decode("UTF-8")))
            item['content']=extract_content(Selector(text=response.body.decode("UTF-8")))
            item['img_url'] = extract_img(Selector(text=response.body.decode("UTF-8")))
            item['type'] = extract_type(response.url,"cankaoxiaoxi")
            write_sys(item['title'])
            next_page=Selector(text=response.body.decode("UTF-8")).xpath("//div[@class='page']/ul//li/a[@id='next_page']/@href").extract()
            yield Request(url=next_page[0], callback=self.relate_page)
            yield item


from newsCrawl.config.config import all_rules
import re
import time
import urllib.request
from scrapy.selector import Selector
#提取摘要
def extract_abstract(hsel):
    item = {}
    rule_abstract=all_rules.rule_abstract
    rules=rule_abstract.values()
    for rule in rules:
        abstract=hsel.xpath(rule['xpath']).extract()
        if len(abstract)>0:
            item['abstract']=re.findall(rule['regex'],abstract[0])[0]
            break
        item['abstract']=''
    return item['abstract']
#提取标题
def extract_title(hsel):
    item = {}
    rule_title=all_rules.rule_title
    rules=rule_title.values()
    for rule in rules:
        title=hsel.xpath(rule['xpath']).extract()
        if len(title)>0:
            for i in (rule['regex'].split('|')):
                item['title']=title[0].replace(i,"")
            break
        item['title']=''
    return item['title']
#提取时间
def extract_time(hsel):
    item = {}
    rule_time=all_rules.rule_time
    rules=rule_time.values()
    for rule in rules:
        newstime=hsel.xpath(rule['xpath']).extract()
        if len(newstime)>0:
            item['time']=time.strftime('%Y-%m-%d %H:%M:%S',(time.strptime(re.findall(rule['regex'],newstime[0])[0],rule['format'])))
            break
        item['time']=''
    return item['time']
#提取来源
def extract_source(hsel):
    item = {}
    rule_source=all_rules.rule_source
    rules=rule_source.values()

    for rule in rules:
        source=hsel.xpath(rule['xpath']).extract()
        if len(source)>0:
            item['source']=re.findall(rule['regex'],source[0])[0]
            break
        item['source']=''
    return item['source']
#提取图片
def extract_img(hsel):
    item = {}
    rule_img=all_rules.rule_img
    rules=rule_img.values()
    for rule in rules:
        img=hsel.xpath(rule['xpath']).extract()
        if len(img)>0:
            item['img']=re.findall(rule['regex'],img[0])[0]
            break
        item['img']=''
    return item['img']
#提取类型
def extract_type(url,name):
    item = {}
    web=all_rules.channel[name]
    regexs=web['regex'].values()
    for regex in regexs:
        if re.match(regex,url):
            t = re.match(regex, url).group(1)
            try:
                item['type']=web['channel'][t]
            except:
                item['type'] = ''
            break
        item['type'] = ''
    return item['type']
#提取正文
def extract_content(hsel):
    item={}
    rule_content=all_rules.rule_content
    rules=rule_content.values()
    contents=""
    for rule in rules:
        content=hsel.xpath(rule['xpath']).extract()
        if len(content)>0:
            contents+=("".join(content)).replace('\u3000',"").replace('\xa0',"")
    item['content']=contents
    return item['content']

if __name__=='__main__':
    # pass
    response=urllib.request.urlopen('http://finance.chinanews.com/cj/2019/01-09/8724287.shtml')
    t=response.read().decode('gbk')
    print(t)
    hh=Selector(text=t)
    print(extract_title(hh))
    print("djfsdkf"+str(int(time.time())))
    # # print(hh.xpath('//p[@class="photo-description"]/text()').extract()[0]+"dkjkjkj")
    # # print(extract_type("http://military.people.com.cn/n1/2018/1228/c1011-30493445.html","people"))
    # times = hh.xpath('//span[@class="source"]/text()').extract()
    # titles = hh.xpath("//ul[@class='txt-list-a fz-14 clear']//li/a/text()").extract()
    # urls = hh.xpath("//ul[@class='txt-list-a fz-14 clear']//li/a/@href").extract()

    # print(extract_source(hh))
    # print(extract_title(hh))
    # print(extract_content(hh))




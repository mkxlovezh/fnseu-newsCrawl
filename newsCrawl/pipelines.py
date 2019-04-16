# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import uuid
from newsCrawl.logs.logtools import write_err
from newsCrawl.logs.logtools import write_info
import requests
from kafka import KafkaProducer
import json
class NewscrawlPipeline(object):
    # def __init__(self):
    #     print('jjjjj')
    #     try:
    #         self.conn=pymysql.connect(host="223.3.76.68",user="root",password="root",db='zhihuhot')
    #     except Exception as e:
    #         print(repr(e))
    #     else:
    #         self.cursor=self.conn.cursor()
    # # def close_spider(self,spider):
    # #     self.conn.close()
    # def process_item(self, item, spider):
    #     url=item['url']
    #     title=item['title']
    #     time=item['time']
    #     source=item['source']
    #     img=item['img_url']
    #     write_err(title)
    #     abstract=item['abstract']
    #     type=item['type']
    #     content=item['content']
    #     id=str(uuid.uuid1())
    #     try:
    #         self.cursor.execute('insert into allnews (url,title,time,source,img,abstract,type,content) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',(url,title,time,source,img,abstract,type,content))
    #         self.conn.commit()
    #     except Exception as e:
    #         print(repr(e))
    #     return item
    def process_item(self, item, spider):
        url = item['url']
        title = item['title']
        time = item['time']
        source = item['source']
        img_url = item['img_url']
        abstract = item['abstract']
        type = item['type']
        content = item['content'].replace('null','')
        id=str(uuid.uuid1())
        data={

            "add":{
                "doc":{
                    "id":id,
                    "url":url,
                    "title":title,
                    'status':0,
                    "time":time,
                    "source":source,
                    "img":img_url,
                    "abstract":abstract,
                    "ctype":type,
                    "content":title+"."+content,
                }
            }
        }
        params={"boost":1.0,'overwrite':'true','commitWithin':1000}
        url="http://seu:8983/solr/real-news/update?_=1547017612245&commitWithin=1000&overwrite=true&wt=json"
        headers={"Content-type":"application/json"}
        r=requests.post(url,json=data,params=params,headers=headers)
        print(r.status_code)
        if r.status_code==200:
            write_info("插入正确:"+item['url'])
            producer=KafkaProducer(bootstrap_servers='seu:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
            try:
                print(id)
                producer.send('new-docId-input',{
                    "doc_id":str(id)
                })
                producer.flush()
            except Exception as e:
                write_err("error")
        else:
            write_err("插入错误："+item['url'])

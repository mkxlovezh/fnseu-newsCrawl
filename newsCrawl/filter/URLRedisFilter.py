import redis
from scrapy.dupefilter import BaseDupeFilter
from scrapy.utils.request import request_fingerprint
class DupFilter(BaseDupeFilter):
    def __init__(self):
        try:
            self.conn=redis.Redis(host='223.3.71.162',port=6379,db=2)
        except:
            print("数据库连接失败")
    def request_seen(self, request):
        fid=request_fingerprint(request)
        result=self.conn.sadd("visited_urls",fid)
        if result==1:
            return False
        return True
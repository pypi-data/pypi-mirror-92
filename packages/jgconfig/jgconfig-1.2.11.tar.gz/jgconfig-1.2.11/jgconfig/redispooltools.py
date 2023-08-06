import redis

class RedisPoolTools:
    selfpool=None

    @staticmethod
    def initPools(host='127.0.0.1',port=6379,password=None):
        RedisPoolTools.selfpool = redis.ConnectionPool(host=host, port=port,password=password, decode_responses=True)

    def __init__(self,sign=''):
        self.rd = redis.Redis(connection_pool=RedisPoolTools.selfpool)
        self.sign = sign

    def StringSet(self,key,val,ex=None):
        self.rd.set(self.sign+ key, val,ex=ex)
    
    def StringGet(self,key):
        return self.rd.get(self.sign + key)

    def HasSet(self,haskey,key,val,ex=None):
        self.rd.hset(self.sign + haskey,key,val,ex)

    def HasGet(self,haskey,key):
        return self.rd.hget(self.sign + haskey,key)

    # def timeout(self):
    #     self.rd.t

    def HasAll(self,name):
        return self.rd.hgetall(self.sign + name)

    def incr(self,key:str,add:int=1):
        return self.rd.incr(self.sign + key,add)

    def timeout(self,name,sec):
        self.rd.expire(self.sign + name,sec)

    def RomveKey(self,name):
        self.rd.delete(self.sign + name)

    def GetStrFromHasByte(self,hs,hname):
        try:
            return str(hs[bytes(hname, encoding = "utf8")],encoding="utf-8")
        except:
            pass
        return ''

    def DeQueue(self,name):
        return self.rd.lpop(self.sign + name)

    def EnQueue(self,name,val1):
        self.rd.lpush(self.sign + name,val1)

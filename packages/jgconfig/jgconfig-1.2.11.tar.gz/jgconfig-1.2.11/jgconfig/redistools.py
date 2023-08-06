import redis

class RedisTools:
    def __init__(self,host='localhost',port=6379,db=0,pwd=None):
        self.rd = redis.StrictRedis(host=host, port=6379, db=0,password=pwd)

    def StringSet(self,key,val,ex=None):
        self.rd.set(key, val,ex=ex)
    
    def StringGet(self,key):
        return self.rd.get(key)

    def HasSet(self,haskey,key,val,ex=None):
        self.rd.hset(haskey,key,val,ex)

    def HasGet(self,haskey,key,val):
        return self.rd.hget(haskey,key)

    # def timeout(self):
    #     self.rd.t

    def HasAll(self,name):
        return self.rd.hgetall(name)
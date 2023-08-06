
import requests
import datetime


class DingDingPush:

    @staticmethod
    def pushMsg(dingdingpushURLS:str,content:str,isAtAll=True) -> str:
        inow = datetime.datetime.now()
        jsonReq = {
            "msgtype": "text", 
            "text": {
                "content": f'[{inow}]::{content}'
            }, 
            "at": {
                # "atMobiles": [
                #     "156xxxx8827", 
                #     "189xxxx8325"
                # ], 
                "isAtAll": isAtAll
            }
        }

        bak = requests.post(dingdingpushURLS,json=jsonReq )
        return bak

    def __init__(self,pushurl:str, titles:str ):
        self.msgs = ''
        self.pushurl = pushurl
        self.title = titles

    def addmd(self,msg):
        self.msgs = self.msgs + msg + '\n'

    def pushmd(self) -> (str, str):

        jsonReq = {
            "msgtype": "markdown",
            "markdown": {
                "title": self.title,
                "text": self.msgs
            },
            "at": {
                # "atMobiles": [
                #     "17707640806"
                # ], 
                "isAtAll": True
            }
        }

        tmpmsgs = self.msgs
        bak = requests.post(self.pushurl,json=jsonReq )
        self.msgs = ''
        return bak, tmpmsgs

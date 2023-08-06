import json
import os
import requests


ConfigJson={}


class ConfigServer:
    CONFIG={}

    @staticmethod
    def initConfig(filename='jgconfig.json'):
        if os.path.exists(filename) is False:
            with open(filename,'w+',encoding='utf-8') as fs:
                fs.write(json.dumps({"serverurl":"m1"}))
        with open(filename,'r',encoding='utf-8') as fs:
            confistr = fs.read()
        
        ConfigJson = json.loads(confistr)
        print('ConfigJson')
        print(ConfigJson)
        return ConfigJson

    @staticmethod
    def getNowVal(geturl:str,fapp:str,fkey:str):
        url = f'{geturl}/getval?fapp={fapp}&fkey={fkey}'
        b = requests.get(url)
        bjson = json.loads(b.text)
        if str(bjson['code']) == '200':
            return bjson['data']
        return False

    @staticmethod
    def Init(geturl=None):
        '''
            request = url

            {
                "code": "200",
                "msg": "ok",
                "data": [
                    {
                    "id": 1,
                    "fapp": "checkoneminute",
                    "fkey": "ison",
                    "fval": "1",
                    "fremark": "1：开，0：关闭"
                    },
                    {
                    "id": 2,
                    "fapp": "checkoneminute",
                    "fkey": "demo",
                    "fval": "1",
                    "fremark": "1：开，0：关闭"
                    }
                ]
            }
        '''
        if geturl is None:
            geturl = ConfigJson['serverurl']
        bak = requests.get(geturl)
        print(bak.text)
        jsonbak = json.loads(bak.text)
        if int(jsonbak['code']) != 200:
            raise Exception('配置服务器错误')

        for v in jsonbak['data']:
            ConfigServer.CONFIG[v['fkey']] = v['fval']

        return ConfigServer.CONFIG

    




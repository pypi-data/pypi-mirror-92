import hashlib


class StringTools:
    def __init__(self):
        pass

    @staticmethod
    def getMd5(data:str) -> str:
        return hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()


if __name__ == '__main__':
    kl = StringTools.getMd5('123456')
    print(kl)
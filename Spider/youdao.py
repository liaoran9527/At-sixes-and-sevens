import hashlib
import random
import time
from pprint import pprint
import requests


class YouDaoSpider(object):

    def __init__(self, word):
        self.url = "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
            "Cookie": "OUTFOX_SEARCH_USER_ID=2004598202@10.108.160.19; OUTFOX_SEARCH_USER_ID_NCOO=111942816.21549504; JSESSIONID=aaalkwd4SZoaA9oUjCimx; SESSION_FROM_COOKIE=unknown; ___rl__test__cookies=1593574712243",
            "Referer": "http://fanyi.youdao.com/"
        }
        self.formdata = {}
        self.word = word

    def generate_formdata(self):
        """
        生成请求体字典的方法
        :return:
        """
        """
         r = 
         i = r + parseInt(10 * Math.random(), 10);
        ts: "" + (new Date).getTime()   生成13位的时间戳 （字符串）
        salt: ts + parseInt(10 * Math.random(), 10);  
        sign: n.md5("fanyideskweb" + e + i + "mmbP%A-r6U3Nw(n]BjuEU")
            e: 要翻译的内容  上午好
            i ： salt
        """
        # 1. 生成ts的值：  生成13位的时间戳 （字符串）
        # 因为生成的时间戳是 10位带小数点的 --- 需要的是 13位的
        # 乘以1000之后还是带小数点，但是13位整数时间戳  类型转换成int
        # 由于需要在此时间戳后面拼接一个 0-9随机数 转换成 str类型
        ts = str(int(time.time() * 1000))
        # 由于生成的随机数是整数  不能和 ts 字符串直接相加 所以转换成了str类型
        salt = ts + str(random.randint(0, 9))

        temp_str = "fanyideskweb" + self.word + salt + "mmbP%A-r6U3Nw(n]BjuEU"
        # 创建MD5对象
        MD5 = hashlib.md5()
        # 调用update方法传入数据的bytes类型
        MD5.update(temp_str.encode())
        # 调用hexdigest方法取出加密之后的16进制的字符串
        sign = MD5.hexdigest()

        self.formdata = {
            "i": self.word,
            "from": "AUTO",
            "to": "AUTO",
            "smartresult": "dict",
            "client": "fanyideskweb",
            "salt": salt,
            "sign": sign,
            "ts": ts,
            "bv": "b286f0a34340b928819a6f64492585e8",
            "doctype": "json",
            "version": "2.1",
            "keyfrom": "fanyi.web",
            "action": "FY_BY_REALTlME"
        }

    def send_request(self):
        """
        发送请求 获取响应数据
        :return:
        """
        response = requests.post(self.url, headers=self.headers, data=self.formdata)
        return response.json()

    def parse_data(self, response):
        """
        解析响应的方法
        :param response: 响应的内容（dict）
        :return:
        """
        # print(response)
        result = response["translateResult"][0][0]["tgt"]
        print(f"{self.word} 的翻译结果是： {result}")

    def run(self):
        # 1. 准备url地址  init方法中已经准备好了
        # 2. 生成请求体字典
        self.generate_formdata()
        # pprint(self.formdata)
        # 3. 发送请求 获取响应
        response = self.send_request()
        # 4. 解析响应
        self.parse_data(response)


if __name__ == '__main__':
    word = input("请输入要翻译的内容：")
    youdao = YouDaoSpider(word)
    youdao.run()

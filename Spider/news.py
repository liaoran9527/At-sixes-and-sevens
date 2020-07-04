import requests
from lxml import etree
import time


class SinaSpider(object):

    def __init__(self):
        self.url = "http://mil.news.sina.com.cn/roll/index.d.html?cid=57918&page=1"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
        }

    def send_request(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content.decode()

    def parse_data(self, response):
        # 转换element对象
        element = etree.HTML(response)
        li_list= element.xpath('//ul[@class="linkNews"]/li')
        for li in li_list:
            title = li.xpath("./a/text()")[0]
            print(title)

        next_url = element.xpath("//a[text()='下一页']/@href")[0]
        return next_url

    def run(self):
        # 1. 准备url
        # 2. 发送请求获取响应
        next_url = self.url
        while True:
            time.sleep(2)
            response = self.send_request(next_url)
            # 3. 解析数据
            next_url = self.parse_data(response)


if __name__ == '__main__':
    sina = SinaSpider()
    sina.run()
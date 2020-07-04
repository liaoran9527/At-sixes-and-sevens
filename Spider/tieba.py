import requests
from lxml import etree
from pprint import pprint


class TieBaSpider(object):

    def __init__(self, name):
        self.url = "https://tieba.baidu.com/f?ie=utf-8&kw={}".format(name)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"}

    def send_request(self, url):
        """
        发送请求 获取响应的方法
        :param url: 发送请求的url地址
        :return: 响应的内容
        """
        response = requests.get(url, headers=self.headers)
        return response.content

    def parse_data(self, response):
        """
        数据解析的方法
        :param response: 响应的内容bytes类型
        :return: 提取出来的数据
        """

        # 将html中被注释掉的内容进行替换
        response = response.decode().replace('<!--', "").replace("-->", "")

        print("开始解析数据。。。。。。。")
        # 1. 将html源码转换成element对象
        element = etree.HTML(response)
        # 2. 对数据进行分组
        li_list = element.xpath("//ul[@id='thread_list']/li")
        # print(li_list)
        # 遍历li_list取出每一个li标签进行提取数据
        content_list = []
        for li in li_list:
            item = {}
            item['title'] = li.xpath('.//a[@class="j_th_tit "]/text()')[0]
            item['detail_url'] = "https://tieba.baidu.com" + li.xpath('.//a[@class="j_th_tit "]/@href')[0]
            # 发送详情页的url地址，拿到详情页的响应
            # print(item)
            detail_response = self.send_request(item['detail_url'])
            # 解析详情页的内容
            item['image_url_list'] = self.parse_detail(detail_response)
            self.save_img(item['image_url_list'])

    def save_img(self, image_url_list):
        """
        保存图片的方法
        :param image_url_list:
        :return:
        """
        # 1. 发送图片的Url地址请求，获取到图片的响应
        for image_url in image_url_list:
            response = self.send_request(image_url)
             # 2. 包响应的bytes类型进行保存
            img_name = image_url[90:]
            with open("images/ "+img_name, "wb") as f:
                print(f"正在保存。。。{img_name}")
                f.write(response)

    def parse_detail(self, response):
        """
        解析详情页的响应的方法
        :param response: 详情页的响应内容
        :return: 图片的地址
        """
        # 1. 将响应内容转换成element对象
        element = etree.HTML(response)
        # 2. 调用xpath方法去解析数据
        image_url_list = element.xpath("//img[@class='BDE_Image']/@src")
        return image_url_list

    def run(self):
        # 1. 准备url地址 请求头信息
        # 2. 发送请求 获取响应
        response = self.send_request(self.url)
        # 3. 提取数据
        self.parse_data(response)


if __name__ == '__main__':
    name = input("请输入要抓取的贴吧名字：")
    tieba = TieBaSpider(name)
    tieba.run()

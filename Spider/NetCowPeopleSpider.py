"""
1.准备url
2.发出请求，获取响应
3.找到详细页面，发出请求获取响应
4.保存图片
"""
import requests
from lxml import etree



class NCPSpider(object):

    def __init__(self):
        self.url = "https://ss.netnr.com/wallpaper#"
        self.headers ={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"}


    def send_requests(self,url):
        response = requests.get(url,headers = self.headers)
    #    print(response.content)
        return response.content
    def parse_data(self,response):
        """
        数据解析的方法
        :param response: 响应的内容bytes类型
        :return: 提取出来的数据
        """
        response = response.decode().replace('<!--', "").replace("-->", "")
      #  print("正在解析内容......")
        # 1. 将html源码转换成element对象
        element = etree.HTML(response)
        # 2. 对数据进行分组
        div_list = element.xpath("//div[@class = 'container-fluid divWP/div']")
        # print(li_list)
        # 遍历li_list取出每一个li标签进行提取数据
        content_list = []
        for div in div_list:
            item = {}
            item['title'] = div.xpath('.//a[@class="j_th_tit "]/text()')[0]
            item['detail_url'] = "https://tieba.baidu.com" + div.xpath('.//a[text() = ▼1600x900]/@href')[0]
            # 发送详情页的url地址，拿到详情页的响应
            # print(item)
            detail_response = self.send_request(item['detail_url'])
            # 解析详情页的内容
            item['image_url_list'] = self.parse_detail(detail_response)
            self.save_img(item['image_url_list'])
    def parse_detail(self,response):
        """
        解析详情页的响应的方法
        :param response: 详情页的响应内容
        :return: 图片的地址
        """
        element = etree.HTML(response)
        img_url_list = element.path("//img[@width = '614']/@src")
    def save_img(self,img_url_list):
        for imge_url in img_url_list:
            response = self.send_requests(imge_url)
            # img_name = imge_url[90:]
        with open("pictures/ "+  "wb") as f:
             # print(f"正在保存。。。{img_name}")
             f.write(response.decode())
    def run(self):
        # 1. 准备url地址 请求头信息
        # 2. 发送请求 获取响应
        response = self.send_requests(self.url)
        # 3. 提取数据
        self.parse_data(response)
if __name__ =='__main__':
    spider = NCPSpider()
    spider.run()
import requests


class King(object):

    def __init__(self, word):
        self.url = "http://fy.iciba.com/ajax.php?a=fy"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
        }
        self.word = word
        # 发送的是一个post请求 额外准备好请求体参数的字典
        self.form_data = {
            'f': "auto",
            't': "auto",
            'w': word
        }

    def send_request(self):
        """
        发送请求 获取响应的方法
        :return:
        """
        response = requests.post(self.url, headers=self.headers, data=self.form_data)
        return response.json()

    def parse_data(self, response):
        """
        解析数据的方法
        :param response: 网页的响应内容（已经被转换成python类型）
        :return:
        """
        try:
            result = response['content']['out']
        except Exception as e:
            result = response['content']['word_mean']
        print(f'{self.word} 的翻译结果是：{result}')

    def run(self):
        # 实现爬虫的主要业务逻辑
        # 1. 准备url地址
        # 2. 发送请求获取响应
        response = self.send_request()
        # 3. 解析数据
        self.parse_data(response)


if __name__ == '__main__':
    king = King("Noodles")
    king.run()

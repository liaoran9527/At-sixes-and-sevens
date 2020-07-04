import requests

# 1. 准备好图片的url地址
url = "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1593412904018&di=29a80c186b322b3b632810f2869011f9&imgtype=0&src=http%3A%2F%2Fimg1.juimg.com%2F160810%2F330750-160Q011125350.jpg"
# 2. 发送图片的url地址请求 获取响应
response = requests.get(url)

# 3. 将响应数据保存本地图片   以字符串写入文件  以二进制方式写入文件？

# 图片 音频 视频 保存的时候 二进制方式进行保存    wb
with open("reba.png", "wb") as f:
    f.write(response.content)
from pprint import pprint

import requests
url = "https://bird.ioliu.cn/v2?url=http%3A%2F%2Fwallpaper.apc.360.cn%2Findex.php%3Fc%3DWallPaper%26start%3D1%26count%3D12%26from%3D360chrome%26a%3DgetAppsByOrder%26order%3Dcreate_time"
headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"}
response = requests.get(url,headers = headers)
res = response.json()
# response = response.decode().replace("<!-- https://github.com/netnr https://gitee.com/netnr https://www.netnr.com https://zme.ink -->", "")
# print(res['data'][i]['img_1600_900'])
for i in range(12):
       # img_name = i
       pictures_url = res['data'][i]['img_1600_900']
       requests1 = requests.get(pictures_url,headers = headers)
       with open("34324"+i, "wb") as f:
           f.write(requests1.content)

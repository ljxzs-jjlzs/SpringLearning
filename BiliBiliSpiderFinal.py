import json
import os
import pymysql
import requests
from pyquery import PyQuery as pq
from datetime import datetime

'''
准备工作：安装上面的外部库函数以及安装mysql或者使用远程的mysql
使用方法：直接调用main函数即可,如果无法成功运行需要自己更改init函数中的cookie字段， 注意在save_database函数中,
        你需要根据自己主机的用户名，密码，端口进行更改，也可以连接到其他电脑上的mysql，但是需要提供相应ip在host参数
更新时间:2022/7/21
'''


class BiliBiliSpider:
    def __init__(self, build_time):
        self.url = "https://www.bilibili.com/v/popular/rank/all"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36",
            "Host": "www.bilibili.com",
            "Cookie": "buvid3=F13314C9-AF05-496D-A3C0-4B247A199112185001infoc; rpdid=|(u)YlJll)u)0J'uYu~YJJkm~; LIVE_BUVID=AUTO3016343808687562; video_page_version=v_old_home_19; i-wanna-go-back=-1; b_ut=5; fingerprint_s=68046f4568cfbab55f51fc28109762a1; buvid4=4A39FC5C-4168-67C6-6D67-859C7FA174A905472-022012817-HNYvTHSPdBRCTHR18+VOkOMvW5cR8Z9C62xxuHRNb+6cV9PrxjZ42Q%3D%3D; CURRENT_BLACKGAP=0; nostalgia_conf=-1; _uuid=D698916F-67D7-7ADD-E10FC-7B88F10E9AA1F33459infoc; sid=kfb7us6h; buvid_fp_plain=undefined; buvid_fp=eb1df20a7e85fc46c61d5b22c8c6f33b; DedeUserID=1949176674; DedeUserID__ckMd5=a438570ff00c9dca; SESSDATA=cbe52d64%2C1666338176%2Cd7f5f*41; bili_jct=06e382163bf2abbc3b75317f4a90b71b; fingerprint3=ca34d11de814b22192d202ddf672e74c; fingerprint=eb1df20a7e85fc46c61d5b22c8c6f33b; blackside_state=0; CURRENT_QUALITY=112; PVID=1; bp_video_offset_1949176674=681082230134538200; b_lsid=2104575CC_182195718EC; bsource=search_google; innersign=1; CURRENT_FNVAL=4048; theme_style=light; b_timer=%7B%22ffp%22%3A%7B%22333.337.fp.risk_F13314C9%22%3A%2218219571CC6%22%2C%22333.1007.fp.risk_F13314C9%22%3A%221821957F9BE%22%2C%22333.934.fp.risk_F13314C9%22%3A%221821957FB3D%22%2C%22333.788.fp.risk_F13314C9%22%3A%22182195B4B87%22%2C%22333.999.fp.risk_F13314C9%22%3A%22182195C10AC%22%7D%7D"
        }
        self.html = None
        self.result = None
        self.today = str(build_time.strftime("%d_%b_%Y"))
        if not os.path.exists("./BiliBili"):
            # print("已经建立文件夹")
            os.mkdir('./BiliBili')
        self.filename = './BiliBili/BiliBili' + self.today + '.json'
        self.filename_ = './BiliBili/BiliBili' + str(build_time.strftime("%Y_%m_%d_%H")) + '.json'
        self.build_time = build_time

    def get_page(self):
        response = requests.get(self.url, headers=self.headers)
        response.encoding = 'utf-8'
        # print(type(response))
        if response.status_code == 200:
            print("Successfully Get Page!")
            self.html = response.text
        else:
            self.html = None

    def parse_page(self):
        doc = pq(self.html)
        results = doc.find('.rank-item')
        target = []
        i = 1
        for result in results:
            temp_target = {}
            temp = pq(result)
            temp_target["index_s"] = i
            temp_target["titles"] = temp.find('.title').text()
            # temp_target.append(temp.find('.title').text())
            # print(temp.find('.title').text())
            temp_target["link"] = temp.find('.title').attr("href")
            # temp_target.append(temp.find('.title').attr("href"))
            # print(temp.find('.title').attr("href"))
            temp_str = temp.find('.detail-state').text().split(' ')
            temp_target["play_volume"] = temp_str[0]
            temp_target["comments"] = temp_str[1]
            temp_target["build_time"] = str(self.build_time.strftime("%Y/%m/%d/%H:%M:%S"))
            # for i_str in temp_str:
            #     temp_target.append(i_str)
            target.append(temp_target)
            i += 1
            # print(temp.find('.detail-state').text())
        self.result = target

    def save_json(self):
        with open(self.filename, "w", encoding='utf-8') as f:
            f.write(json.dumps(self.result, indent=2, ensure_ascii=False))
        with open(self.filename_, 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.result, indent=2, ensure_ascii=False))

    def save_database(self, host="localhost", user='root', password='123456', port=3306):
        with open(self.filename, "r", encoding='utf-8') as f:
            datas = json.loads(f.read())
        db = pymysql.connect(host=host, user=user, password=password, port=port)
        cursor = db.cursor()
        cursor.execute('CREATE DATABASE IF NOT EXISTS bilibili DEFAULT CHARACTER SET utf8mb4')
        cursor.execute('USE bilibili')
        table = 'bilibili_heat' + self.today
        cursor.execute(
            f'CREATE TABLE IF NOT EXISTS {table} (index_s INT NOT NULL, titles VARCHAR(255) NOT NULL, '
            f'link VARCHAR(255) NOT NULL, play_volume VARCHAR(255), comments VARCHAR(255),'
            f' build_time VARCHAR(255) NOT NULL,'
            ' PRIMARY KEY (index_s))'.format(table=table))
        keys = ','.join(datas[0].keys())
        values = ','.join(['%s'] * len(datas[0]))
        sql = f'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'.format(table=table, keys=keys,
                                                                                              values=values)
        update = ','.join([" {key} = %s".format(key=key) for key in datas[0]])
        sql += update
        try:
            for data in datas:
                if cursor.execute(sql, tuple(data.values()) * 2):
                    print("SUCCESSFULLY!")
                    db.commit()
        except Exception as e:
            print(e.args)
            print("Error")
        db.close()
        with open(self.filename_, "r", encoding='utf-8') as f:
            datas = json.loads(f.read())
        db = pymysql.connect(host=host, user=user, password=password, port=port)
        cursor = db.cursor()
        cursor.execute('CREATE DATABASE IF NOT EXISTS bilibili DEFAULT CHARACTER SET utf8mb4')
        cursor.execute('USE bilibili')
        table = 'bilibili_heat' + str(self.build_time.strftime("_%Y_%m_%d_%H"))
        cursor.execute(
            f'CREATE TABLE IF NOT EXISTS {table} (index_s INT NOT NULL, titles VARCHAR(255) NOT NULL, '
            f'link VARCHAR(255) NOT NULL, play_volume VARCHAR(255), comments VARCHAR(255),'
            f' build_time VARCHAR(255) NOT NULL,'
            ' PRIMARY KEY (index_s))'.format(table=table))
        keys = ','.join(datas[0].keys())
        values = ','.join(['%s'] * len(datas[0]))
        sql = f'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'.format(table=table, keys=keys,
                                                                                              values=values)
        update = ','.join([" {key} = %s".format(key=key) for key in datas[0]])
        sql += update
        try:
            for data in datas:
                if cursor.execute(sql, tuple(data.values()) * 2):
                    print("SUCCESSFULLY!_")
                    db.commit()
        except Exception as e:
            print(e.args)
            print("Error")
        db.close()


    def main(self):
        self.get_page()
        self.parse_page()
        self.save_json()
        self.save_database()


if __name__ == "__main__":
    bilibili = BiliBiliSpider(datetime.now())
    bilibili.main()

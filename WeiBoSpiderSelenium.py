import os
from datetime import datetime
import pymysql
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import time


class WeiBoSpider:
    def __init__(self, build_time):
        self.url = "https://s.weibo.com/top/summary?cate=realtimehot"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36",
            "Host": "s.weibo.com",
            "Cookie": 'SINAGLOBAL=5746989199853.571.1633253950194; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWDo0purAGdEIQBaNdc4AJs5JpX5KMhUgL.Foqpeo5ESKnNSo.2dJLoI7f_wPSLds9keo5pe054; ALF=1690026379; SSOLoginState=1658490380; SCF=Alm1wPbesWa7AHMsTieisMPSr6c2O55edmj_R9V3nCfLOGHCYWvxvoDSSJb0OULwgTUXjQMRvqBWUT1lnyJgfsM.; SUB=_2A25P3v5dDeRhGeBP6VIT9SbLzTWIHXVsqmiVrDV8PUNbmtANLW77kW9NRW_6Xg-rbYmA06KROlgsCKttPN3p_cS8; _s_tentry=login.sina.com.cn; UOR=,,login.sina.com.cn; Apache=25869256750.66354.1658490381778; ULV=1658490381792:8:6:4:25869256750.66354.1658490381778:1658374234416'
        }
        self.html = None
        self.result = []
        self.today = str(build_time.strftime("%d_%b_%Y"))
        if not os.path.exists("./WeiBo"):
            # print("已经建立文件夹")
            os.mkdir('./WeiBo')
        self.filename = './WeiBo/WeiBo' + self.today + '.json'
        self.filename_ = './WeiBo/WeiBo' + str(build_time.strftime("%Y_%m_%d_%H")) + '.json'
        self.build_time = build_time

    def get_page(self):
        driver = webdriver.Chrome()
        self.result = []
        driver.get(self.url)
        driver.maximize_window()
        time.sleep(10)
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(5)
        items = driver.find_elements(By.CSS_SELECTOR, '#pl_top_realtimehot table tbody tr')
        # print('此时的len: ', len(items))
        while len(items) < 50:
            # print('此时的len: ', len(items))
            time.sleep(3)
            items = driver.find_elements(By.CSS_SELECTOR, '#pl_top_realtimehot table tbody tr')
        # print(items)
        # number = 51
        for item in items:
            target = {}
            index = item.find_element(By.CSS_SELECTOR, '.td-01').text
            if index == '':
                index = 0
            else:
                try:
                    index = int(index)
                except:
                    continue

            target['index_s'] = index
            try:
                heat = item.find_element(By.CSS_SELECTOR, '.td-02 span').text
                heat = heat.split(' ')[-1]
            except:
                heat = 'unknown'
            target['heat'] = heat
            title = item.find_element(By.CSS_SELECTOR, '.td-02 a').text
            target['title'] = title
            target['links'] = item.find_element(By.CSS_SELECTOR, '.td-02 a').get_attribute('href')
            target['build_time'] = str(self.build_time.strftime("%Y/%m/%d/%H:%M:%S"))
            self.result.append(target)
            # print('此时的result的长度: ', len(self.result))
        driver.close()

    def sava_json(self):
        with open(self.filename, "w", encoding='utf-8') as f:
            f.write(json.dumps(self.result, indent=2, ensure_ascii=False))
        with open(self.filename_, "w", encoding='utf-8') as f:
            f.write(json.dumps(self.result, indent=2, ensure_ascii=False))

    def save_database(self, host="localhost", user='root', password='123456', port=3306):
        with open(self.filename, "r", encoding='utf-8') as f:
            datas = json.loads(f.read())
        db = pymysql.connect(host=host, user=user, password=password, port=port)
        cursor = db.cursor()
        cursor.execute('CREATE DATABASE IF NOT EXISTS weibo DEFAULT CHARACTER SET utf8mb4')
        cursor.execute('USE weibo')
        table = 'weibo_heat' + self.today
        cursor.execute(
            f'CREATE TABLE IF NOT EXISTS {table} (index_s INT NOT NULL, heat VARCHAR(255) NOT NULL, '
            f'title VARCHAR(255) NOT NULL, links VARCHAR(255), build_time VARCHAR(255) NOT NULL,'
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
        with open(self.filename, "r", encoding='utf-8') as f:
            datas = json.loads(f.read())
        db = pymysql.connect(host=host, user=user, password=password, port=port)
        cursor = db.cursor()
        cursor.execute('CREATE DATABASE IF NOT EXISTS weibo DEFAULT CHARACTER SET utf8mb4')
        cursor.execute('USE weibo')
        table = 'weibo_heat' + str(self.build_time.strftime("_%Y_%m_%d_%H"))
        cursor.execute(
            f'CREATE TABLE IF NOT EXISTS {table} (index_s INT NOT NULL, heat VARCHAR(255) NOT NULL, '
            f'title VARCHAR(255) NOT NULL, links VARCHAR(255), build_time VARCHAR(255) NOT NULL,'
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
        while len(self.result) < 50:
            print(len(self.result))
            self.get_page()
        self.sava_json()
        self.save_database()


if __name__ == '__main__':

    now = datetime.now()
    weibo = WeiBoSpider(now)
    weibo.main()
# print(weibo.result)

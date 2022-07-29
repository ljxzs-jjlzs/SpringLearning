import json
import os
import pymysql
from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

'''
准备工作：安装上面的外部库函数以及安装mysql或者使用远程的mysql
使用方法：直接调用main函数即可,如果无法成功运行需要自己更改init函数中的cookie字段， 注意在save_database函数中,
        你需要根据自己主机的用户名，密码，端口进行更改，也可以连接到其他电脑上的mysql，但是需要提供相应ip在host参数
更新时间:2022/7/21
'''


class BiliBiliSpider:
    def __init__(self, build_time):
        self.url = "https://www.bilibili.com/v/popular/rank/all"
        self.html = None
        self.result = []
        self.today = str(build_time.strftime("%d_%b_%Y"))
        if not os.path.exists("./BiliBili"):
            # print("已经建立文件夹")
            os.mkdir('./BiliBili')
        self.filename = './BiliBili/BiliBili' + self.today + '.json'
        self.filename_ = './BiliBili/BiliBili' + str(build_time.strftime("%Y_%m_%d_%H")) + '.json'
        self.build_time = build_time

    def get_page(self):
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(self.url)
        time.sleep(3)
        results = driver.find_elements(By.CSS_SELECTOR, '.rank-item')
        while results is None:
            results = driver.find_elements(By.CSS_SELECTOR, '.rank-item')
            time.sleep(2)
        for result in results:
            text = result.find_element(By.CSS_SELECTOR, '.detail-state').text
            text = text.split('\n')
            target = {'index_s': int(result.get_attribute('data-rank')),
                      'titles': result.find_element(By.CSS_SELECTOR, '.info a').text,
                      'link': result.find_element(By.CSS_SELECTOR, '.info a').get_attribute('href'),
                      'play_volume': text[0], 'comments': text[1],
                      'build_time': str(self.build_time.strftime("%Y/%m/%d/%H:%M:%S"))}
            self.result.append(target)
        driver.close()

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
        self.save_json()
        self.save_database()


if __name__ == "__main__":
    bilibili = BiliBiliSpider(datetime.now())
    bilibili.main()

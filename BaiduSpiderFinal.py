import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import pymysql
import os

'''
准备工作：你需要装上面所需要的库，以及chrome浏览器以及配套的chromedriver以及安装mysql，当然你可以连接远程的mysql
使用方法:首先建立一个类变量，然后请依次调用get_page,save_json,save_database或者直接调用main()，注意在save_database函数中,
        你需要根据自己主机的用户名，密码，端口进行更改，也可以连接到其他电脑上的mysql，但是需要提供相应ip在host参数
更新时间:2022/7/21
'''


class BaiduSpider:
    def __init__(self, build_time):
        # self.today是今天的日期,格式为 %d_%b_%Y 例如：Jul_21_2022
        self.today = str(build_time.strftime("%d_%b_%Y"))
        if not os.path.exists("./Baidu"):
            # print("已经建立文件夹")
            os.mkdir('./Baidu')
        self.filename = "./Baidu/Baidu" + self.today + ".json"
        self.filename_ = './Baidu/Baidu' + str(build_time.strftime("%Y_%m_%d_%H")) + '.json'
        self.url = "https://top.baidu.com/board?tab=realtime"
        self.results = None
        self.build_time = build_time

    def get_page(self):
        browser = webdriver.Chrome()
        browser.get(self.url)
        time.sleep(2)
        results = browser.find_elements(By.CSS_SELECTOR, ".horizontal_1eKyQ")
        while results is None:
            results = browser.find_elements(By.CSS_SELECTOR, ".horizontal_1eKyQ")
            time.sleep(2)
        target = []
        for result in results:
            temp_target = {}
            temp_link = result.find_element(By.CSS_SELECTOR, '.img-wrapper_29V76')
            # print(temp_link.get_attribute('href'))
            temp_target["links"] = temp_link.get_attribute('href')
            temp_heat = result.find_element(By.CSS_SELECTOR, '.hot-index_1Bl1a')
            temp_target["heat"] = temp_heat.text
            # print(temp_heat.text)
            temp_title = result.find_element(By.CSS_SELECTOR, '.c-single-text-ellipsis')
            # print(temp_title.text)
            temp_target["titles"] = temp_title.text
            temp_index = result.find_element(By.CSS_SELECTOR, '.index_1Ew5p')
            # print(temp_index.text)
            if temp_index.text == '':
                temp_target["index_s"] = 0
            else:
                temp_target["index_s"] = int(temp_index.text)
            temp_target["build_time"] = str(self.build_time.strftime("%Y/%m/%d/%H:%M:%S"))
            target.append(temp_target)
        browser.close()
        self.results = target

    def save_json(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            f.write(json.dumps(self.results, indent=2, ensure_ascii=False))
        with open(self.filename_, "w", encoding="utf-8") as f:
            f.write(json.dumps(self.results, indent=2, ensure_ascii=False))

    def save_database(self, host="localhost", user='root', password='123456', port=3306):
        with open(self.filename, "r", encoding='utf-8') as f:
            datas = json.loads(f.read())
        db = pymysql.connect(host=host, user=user, password=password, port=port)
        cursor = db.cursor()
        cursor.execute('CREATE DATABASE IF NOT EXISTS baidu DEFAULT CHARACTER SET utf8')
        cursor.execute('USE baidu')
        table = 'baidu_heat' + self.today
        cursor.execute(
            f'CREATE TABLE IF NOT EXISTS {table} (links VARCHAR(255) NOT NULL, heat VARCHAR(255) NOT NULL, '
            f'titles VARCHAR(255) NOT NULL, index_s INT NOT NULL, build_time VARCHAR(255) NOT NULL,'
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
        cursor.execute('CREATE DATABASE IF NOT EXISTS baidu DEFAULT CHARACTER SET utf8')
        cursor.execute('USE baidu')
        table = 'baidu_heat' + str(self.build_time.strftime("_%Y_%m_%d_%H"))
        cursor.execute(
            f'CREATE TABLE IF NOT EXISTS {table} (links VARCHAR(255) NOT NULL, heat VARCHAR(255) NOT NULL, '
            f'titles VARCHAR(255) NOT NULL, index_s INT NOT NULL, build_time VARCHAR(255) NOT NULL,'
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
    baidu = BaiduSpider(datetime.now())
    baidu.main()

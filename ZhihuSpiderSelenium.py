from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pyautogui
import json
import pymysql
from datetime import datetime
import os

'''
准备工作：安装上面的外部库函数以及安装mysql或者使用远程的mysql
使用方法：直接调用main函数即可,如果无法成功运行需要自己更改init函数中的cookie字段， 注意在save_database函数中,
        你需要根据自己主机的用户名，密码，端口进行更改，也可以连接到其他电脑上的mysql，但是需要提供相应ip在host参数
更新时间:2022/7/21
'''


class ZhiHuSpider:
    def __init__(self, build_time):
        self.url = "https://www.zhihu.com/hot"
        # 用来存储爬取结果
        self.result = []
        # self.today是今天的日期,格式为 %d_%b_%Y 例如：Jul_21_2022
        self.today = str(build_time.strftime("%d_%b_%Y"))
        if not os.path.exists("./ZhiHu"):
            os.mkdir('./ZhiHu')
        if not os.path.exists("./ZhiHuComments"):
            os.mkdir('./ZhiHuComments')
        if not os.path.exists("./ZhiHuCommentsNew"):
            os.mkdir('./ZhiHuCommentsNew')
        self.filename = './ZhiHu/ZhiHu' + self.today + '.json'
        self.filename_ = './ZhiHu/ZhiHu' + str(build_time.strftime("%Y_%m_%d_%H")) + '.json'
        self.html = None
        self.build_time = build_time
        self.driver = None
        self.before = None

    def open(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def close(self):
        self.driver.quit()

    def login(self):
        self.driver.get('https://www.zhihu.com/question/544969213?utm_division=hot_list_page')
        time.sleep(3)
        pyautogui.moveTo(1166, 787, duration=1)
        time.sleep(2)
        pyautogui.click()
        pyautogui.moveTo(939, 630, duration=1)
        time.sleep(2)
        pyautogui.click()
        time.sleep(5)

    def get_comments(self):
        with open(self.filename, 'r', encoding='utf-8') as f:
            datas = json.loads(f.read())
        for data in datas:
            link = data['links']
            self.driver.get(link)
            time.sleep(3)
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(5)
            pyautogui.moveTo(1912, 1016, duration=0.5)
            pyautogui.click()
            pyautogui.moveTo(1912, 500, duration=0.5)
            pyautogui.click()
            time.sleep(3)
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(5)
            items = self.driver.find_elements(By.CSS_SELECTOR, '.AnswerItem')

            targets = []
            for item in items:
                target = {
                    'name': item.find_element(By.CSS_SELECTOR,
                                              'div[class="AuthorInfo"] meta[itemprop="name"]').get_attribute(
                        'content'), 'author_link': item.find_element(By.CSS_SELECTOR,
                                                                     'div[class="AuthorInfo"] meta[itemprop="url"]').get_attribute(
                        'content')}

                data_str = ''
                comments = item.find_elements(By.CSS_SELECTOR, '.RichText p')
                for comment in comments:
                    if comment.get_attribute('class') == 'ztext-empty-paragraph':
                        continue
                    else:
                        data_str = data_str + comment.text + '\n'
                target['comment'] = data_str
                try:
                    target['likes'] = int(item.find_element(By.CSS_SELECTOR, '.VoteButton--up').text.split(' ')[1])
                except:
                    target['likes'] = 0
                if target['likes'] < 300:
                    if len(target['comment']) > 200:
                        target['comment'] = target['comment'][:200] + '...'
                targets.append(target)

            filename = './ZhiHuComments/Comment_' + str(data['index_s']) + '.json'
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(json.dumps(targets, indent=2, ensure_ascii=False))

    def found(self, links):
        for data in self.before:
            if links == data['links']:
                return data['index_s']

        return -1

    def get_comments_part(self):
        with open(self.filename, 'r', encoding='utf-8') as f, open('./ZhiHu/before.json', 'r', encoding='utf-8') as f1:
            datas = json.loads(f.read())
            self.before = json.loads(f1.read())
        for data in datas:
            link = data['links']
            self.driver.get(link)
            answer = self.found(data['links'])
            if answer > -1:
                old_filename = './ZhiHuComments/Comment_' + str(answer) + '.json'
                new_filename = './ZhiHuCommentsNew/Comment_' + data['index_s'] + '.json'
                with open(old_filename, 'r', encoding='utf-8') as f1, open(new_filename, 'w', encoding='utf-8') as f2:
                    f2.write(json.dumps(json.loads(f.read()), indent=2, ensure_ascii=False))
                continue

            time.sleep(3)
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(5)
            pyautogui.moveTo(1912, 1016, duration=0.5)
            pyautogui.click()
            pyautogui.moveTo(1912, 500, duration=0.5)
            pyautogui.click()
            time.sleep(3)
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(5)
            items = self.driver.find_elements(By.CSS_SELECTOR, '.AnswerItem')

            targets = []
            for item in items:
                target = {
                    'name': item.find_element(By.CSS_SELECTOR,
                                              'div[class="AuthorInfo"] meta[itemprop="name"]').get_attribute(
                        'content'), 'author_link': item.find_element(By.CSS_SELECTOR,
                                                                     'div[class="AuthorInfo"] meta[itemprop="url"]').get_attribute(
                        'content')}

                data_str = ''
                comments = item.find_elements(By.CSS_SELECTOR, '.RichText p')
                for comment in comments:
                    if comment.get_attribute('class') == 'ztext-empty-paragraph':
                        continue
                    else:
                        data_str = data_str + comment.text + '\n'
                target['comment'] = data_str
                try:
                    target['likes'] = int(item.find_element(By.CSS_SELECTOR, '.VoteButton--up').text.split(' ')[1])
                except:
                    target['likes'] = 0
                if target['likes'] < 300:
                    if len(target['comment']) > 200:
                        target['comment'] = target['comment'][:200] + '...'
                targets.append(target)

            filename = './ZhiHuCommentsNew/Comment_' + str(data['index_s']) + '.json'
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(json.dumps(targets, indent=2, ensure_ascii=False))

    def get_page(self):
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(self.url)
        time.sleep(3)
        pyautogui.moveTo(1166, 787, duration=1)
        time.sleep(2)
        pyautogui.click()
        pyautogui.moveTo(939, 630, duration=1)
        time.sleep(2)
        pyautogui.click()
        time.sleep(5)
        results = driver.find_elements(By.CSS_SELECTOR, '.HotItem')
        while results is None:
            results = driver.find_elements(By.CSS_SELECTOR, '.HotItem')
            time.sleep(2)
        for result in results:
            target = {'index_s': int(result.find_element(By.CSS_SELECTOR, '.HotItem-rank').text),
                      'titles': result.find_element(By.CSS_SELECTOR, '.HotItem-content a').get_attribute('title'),
                      'heat': (result.find_element(By.CSS_SELECTOR, '.HotItem-metrics').text).split('\n')[0],
                      'links': result.find_element(By.CSS_SELECTOR, '.HotItem-content a').get_attribute('href'),
                      'build_time': str(self.build_time.strftime("%Y/%m/%d/%H:%M:%S"))}
            self.result.append(target)
        driver.close()

    def save_json(self):
        with open(self.filename, "w", encoding='utf-8') as f:
            f.write(json.dumps(self.result, indent=2, ensure_ascii=False))
        # filename_ = './ZhiHu/ZhiHu' + str(self.build_time.strftime("%Y_%m_%d_%H")) + '.json'
        with open(self.filename_, 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.result, indent=2, ensure_ascii=False))

    def save_database(self, host="localhost", user='root', password='123456', port=3306):
        with open(self.filename, "r", encoding='utf-8') as f:
            datas = json.loads(f.read())
        db = pymysql.connect(host=host, user=user, password=password, port=port)
        cursor = db.cursor()
        cursor.execute('CREATE DATABASE IF NOT EXISTS zhihu DEFAULT CHARACTER SET utf8')
        cursor.execute('USE zhihu')
        table = 'zhihu_heat' + self.today
        cursor.execute(
            f'CREATE TABLE IF NOT EXISTS {table} (index_s INT NOT NULL, titles VARCHAR(255) NOT NULL, '
            f'heat VARCHAR(255) NOT NULL, links VARCHAR(255), build_time VARCHAR(255) NOT NULL,'
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
        cursor.execute('CREATE DATABASE IF NOT EXISTS zhihu DEFAULT CHARACTER SET utf8')
        cursor.execute('USE zhihu')
        table = 'zhihu_heat' + str(self.build_time.strftime("_%Y_%m_%d_%H"))
        cursor.execute(
            f'CREATE TABLE IF NOT EXISTS {table} (index_s INT NOT NULL, titles VARCHAR(255) NOT NULL, '
            f'heat VARCHAR(255) NOT NULL, links VARCHAR(255), build_time VARCHAR(255) NOT NULL,'
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
        try:
            self.save_database()
        except:
            self.main()

    def main_all(self):
        self.main()
        self.open()
        self.login()
        self.get_comments()
        self.close()

    def main_part(self):
        self.main()
        self.open()
        self.login()
        self.get_comments_part()
        self.close()


if __name__ == "__main__":
    zhihu = ZhiHuSpider(datetime.now())
    zhihu.main()

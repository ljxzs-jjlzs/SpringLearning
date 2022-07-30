import json
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime


class BiliBiliSpiderComment:
    def __init__(self):
        self.today = str(datetime.now().strftime("%d_%b_%Y"))
        if not os.path.exists("./BiliBiliCommentNew"):
            # print("已经建立文件夹")
            os.mkdir('./BiliBiliCommentNew')
        self.filename_old = "./BiliBiliComment/comment"
        self.filename_new = './BiliBiliCommentNew/comment'
        self.datas = None
        self.data_before = None

    def load_data(self):
        temp_filename = './BiliBili/BiliBili' + self.today + '.json'
        with open(temp_filename, 'r', encoding='utf-8') as f:
            self.datas = json.loads(f.read())
        with open('./BiliBili/BiliBiliBefore.json', 'r', encoding='utf-8') as f:
            self.data_before = json.loads(f.read())

    def get_comments_all(self):
        driver = webdriver.Chrome()
        driver.maximize_window()
        self.load_data()

        for data in self.datas:
            link = data['link']
            driver.get(link)
            time.sleep(5)
            i = 0
            while i < 4:
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                i += 1
                time.sleep(5)

            results = driver.find_elements(By.CSS_SELECTOR, '.reply-item div[class="content-warp"]')
            i = 1
            targets = []
            for result in results:
                target = {'index': i, 'text': result.find_element(By.CSS_SELECTOR, '.root-reply span').text}
                i += 1
                targets.append(target)
            filename = self.filename_new + str(data['index_s']) + '.json'
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(json.dumps(targets, indent=2, ensure_ascii=False))
            print('新热搜', data['index_s'], '已经加载完毕')

        driver.close()

    def get_comments(self):
        driver = webdriver.Chrome()
        driver.maximize_window()
        self.load_data()

        for data in self.datas:
            link = data['link']
            driver.get(link)
            time.sleep(5)
            index_old = self.found_in_before(data['titles'])
            if index_old > 0:
                self.move_from_old(index_old, data['index_s'])
                print('热搜', data['index_s'], '位于上次热搜', index_old)
                continue
            i = 0
            # print('开始了')
            while i < 4:
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                i += 1
                time.sleep(5)

            results = driver.find_elements(By.CSS_SELECTOR, '.reply-item div[class="content-warp"]')
            i = 1
            targets = []
            for result in results:
                target = {'index': i, 'text': result.find_element(By.CSS_SELECTOR, '.root-reply span').text}
                # print(i)
                i += 1
                targets.append(target)
                # print(result.find_element(By.CSS_SELECTOR, '.root-reply span').text)
            filename = self.filename_new + str(data['index_s']) + '.json'
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(json.dumps(targets, indent=2, ensure_ascii=False))
            print('新热搜', data['index_s'], '已经加载完毕')

        driver.close()

    def found_in_before(self, titles):
        for data in self.data_before:
            if data['titles'] == titles:
                return data['index_s']
        return 0

    def move_from_old(self, index_old, index_new):
        old_filename = self.filename_old + str(index_old) + '.json'
        new_filename = self.filename_new + str(index_new) + '.json'
        with open(old_filename, 'r', encoding='utf-8') as f:
            old_data = f.read()

        with open(new_filename, 'w', encoding='utf-8') as f:
            f.write(old_data)

    def move_to_new(self):
        for i in range(1, 101):
            old_filename = self.filename_old + str(i) + '.json'
            new_filename = self.filename_new + str(i) + '.json'
            with open(new_filename, 'r', encoding='utf-8') as f:
                datas = f.read()
            with open(old_filename, 'w', encoding='utf-8') as f:
                f.write(datas)


if __name__ == '__main__':
    t1 = time.time()
    test = BiliBiliSpiderComment()
    test.get_comments()
    t2 = time.time()
    print(t2 - t1, 's')

import os
from datetime import datetime
import pymysql
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import time
import pyautogui


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
        if not os.path.exists("./WeiBoComment"):
            # print("已经建立文件夹")
            os.mkdir('./WeiBoComment')
        if not os.path.exists("./WeiBoCommentNew"):
            # print("已经建立文件夹")
            os.mkdir('./WeiBoCommentNew')
        self.filename = './WeiBo/WeiBo' + self.today + '.json'
        self.filename_ = './WeiBo/WeiBo' + str(build_time.strftime("%Y_%m_%d_%H")) + '.json'
        self.build_time = build_time
        self.driver = None
        self.before = None

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

    def open(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def close(self):
        self.driver.quit()

    def login(self):
        self.driver.get(
            "https://s.weibo.com/weibo?q=%23%E5%90%B4%E5%95%8A%E8%90%8D%E5%8F%97%E5%AE%A1%E7%94%BB%E9%9D%A2%E5%85%AC"
            "%E5%B8%83%23&Refer=top")
        time.sleep(6)
        temp = self.driver.find_element(By.CSS_SELECTOR, '.card-act')
        temp = temp.find_elements(By.CSS_SELECTOR, 'li')[1]
        temp = temp.find_element(By.CSS_SELECTOR, 'a')
        temp.click()
        pyautogui.moveTo(947, 695, duration=3)
        pyautogui.click()
        pyautogui.moveTo(872, 399, duration=3)
        pyautogui.click()
        time.sleep(2)
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[-1])
        time.sleep(5)

    def get_page_comment(self, base_url, index):
        i = 1
        j = 1
        targets = []
        base_url = base_url + '&page='
        while i < 3:
            url = base_url + str(i)
            i += 1
            self.driver.get(url)
            time.sleep(5)
            items = self.driver.find_elements(By.CSS_SELECTOR, '.card-wrap div[class="card"]')
            if not items:
                print('Error!Error!', 'index', index, '没有爬取成功！')
                break
            for item in items:
                temp_item = item
                try:
                    item = item.find_element(By.CSS_SELECTOR, '.card-feed div[node-type="like"]')
                except:
                    continue
                if j == 1:
                    try:
                        button = item.find_element(By.CSS_SELECTOR, 'a[action-type="fl_unfold"]')
                        button_ = button.find_element(By.CSS_SELECTOR, '.wbicon')
                        button_.click()
                        time.sleep(2)
                        content = item.find_element(By.CSS_SELECTOR, 'p[node-type="feed_list_content_full"]').text
                    except:
                        content = item.find_element(By.CSS_SELECTOR, '.txt').text
                else:
                    content = item.find_element(By.CSS_SELECTOR, '.txt').text
                if j == 1:
                    targets.append({'index': j, 'content': content})
                    j += 1
                elif len(content) < 50:
                    targets.append({'index': j, 'content': content})
                    j += 1
                try:
                    button_ = temp_item.find_elements(By.CSS_SELECTOR, '.card-act ul li')[1]
                    button_ = button_.find_element(By.CSS_SELECTOR, 'a')
                    button_.click()
                    time.sleep(2)
                except:
                    i -= 1
                    continue
                comments = temp_item.find_elements(By.CSS_SELECTOR,
                                                   'div[node-type="feed_list_repeat"] .card-review .txt')
                for comment in comments:
                    text = comment.text
                    position = text.index('：')
                    text = text[position + 1:]
                    if text == '' or text == '图片评论 评论配图':
                        continue
                    targets.append({'index': j, 'content': text})
                    j += 1

        filename_ = './WeiBoComment/WeiBoComment' + str(index) + '.json'
        with open(filename_, 'w', encoding='utf-8') as f:
            f.write(json.dumps(targets, indent=2, ensure_ascii=False))
        print(index, '页成功爬取!')

    def main(self):  # 不更新before
        self.get_page()
        while len(self.result) < 50:
            print(len(self.result))
            self.get_page()
        self.sava_json()
        self.save_database()

    def main_all(self):  # 更新before
        self.main()
        self.open()
        self.login()
        filename = './WeiBo/WeiBo' + str(datetime.now().strftime("%d_%b_%Y")) + '.json'
        with open(filename, 'r', encoding='utf-8') as f:
            datas = json.loads(f.read())
        for data in datas:
            self.get_page_comment(data['links'], data['index_s'])

        with open('./WeiBo/before.json', 'w', encoding='utf-8') as f1:
            f1.write(json.dumps(datas, indent=2, ensure_ascii=False))
        self.close()

    def found(self, links: str):
        for data in self.before:
            if data['links'] == links:
                return data['index_s']

        return -1

    def main_part(self):  # 更新before
        self.main()
        self.open()
        self.login()
        filename = './WeiBo/WeiBo' + str(datetime.now().strftime("%d_%b_%Y")) + '.json'
        with open(filename, 'r', encoding='utf-8') as f:
            datas = json.loads(f.read())
        with open('./WeiBo/before.json', 'r', encoding='utf-8') as f:
            self.before = json.loads(f.read())

        for data in datas:
            answer = self.found(data['links'])
            if answer >= 0:
                old_filename = './WeiBoComment/WeiBoComment' + str(answer) + '.json'
                new_filename = './WeiBoCommentNew/WeiBoComment' + str(data['index_s']) + 'json'
                with open(old_filename, 'r', encoding='utf-8') as f1, open(new_filename, 'w', encoding='utf-8') as f2:
                    f2.write(json.dumps(json.loads(f.read()), indent=2, ensure_ascii=False))
                continue

            self.get_page_comment(data['links'], data['index_s'])

        with open('./WeiBo/before.json', 'w', encoding='utf-8') as f1:
            f1.write(json.dumps(datas, indent=2, ensure_ascii=False))

        self.close()


if __name__ == '__main__':
    now = datetime.now()
    weibo = WeiBoSpider(now)
    weibo.main()
# print(weibo.result)

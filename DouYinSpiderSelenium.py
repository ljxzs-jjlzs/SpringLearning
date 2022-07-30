import json
import os.path
import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime


class DouYinSpiderSelenium:
    def __init__(self, build_time):
        self.url = 'https://www.douyin.com/hot'
        self.result = []
        if not os.path.exists('./DouYin'):
            os.mkdir('./DouYin')
        self.filename_comments = './DouYin/DouYinComments'
        if not os.path.exists('./DouYinHeat'):
            os.mkdir('./DouYinHeat')
        self.today = str(build_time.strftime("%d_%b_%Y"))
        self.filename_heat = './DouYinHeat/heat' + self.today + '.json'
        self.filename_heat_ = './DouYinHeat/heat' + str(build_time.strftime("%Y_%m_%d_%H")) + '.json'
        self.build_time = build_time

    def spider_heat(self):
        driver = webdriver.Chrome()
        driver.get(self.url)
        results = driver.find_elements(By.CSS_SELECTOR, '.BHgRhxNh')
        print(len(results))
        while len(results) < 50:
            results = driver.find_elements(By.CSS_SELECTOR, '.BHgRhxNh')
            time.sleep(1)
        i = 0
        targets = []
        for result in results:
            target = {}
            try:
                links = result.find_element(By.CSS_SELECTOR, '.mmjTMnlA')
                target['index_s'] = i
                target['text'] = links.text
                target['links'] = links.get_attribute('href')
                i += 1
                try:
                    heat = result.find_element(By.CSS_SELECTOR, '.GsuT_hjh')
                    target['heat'] = heat.text
                    targets.append(target)
                except:
                    target['heat'] = 'unknown'
                    targets.append(target)
                    continue
            except:
                print('Error!')
                break

        driver.close()
        self.result = targets
        with open(self.filename_heat, 'w', encoding='utf-8') as f:
            f.write(json.dumps(targets, indent=2, ensure_ascii=False))

    def spider_comments(self, url, index):
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(url)
        time.sleep(1)
        pyautogui.moveTo(1145, 424, duration=1)
        time.sleep(1)
        pyautogui.click()
        i = 0
        while i < 14:
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(1)
            i += 1
        results = driver.find_elements(By.CSS_SELECTOR, '.comment-mainContent div[class="CDx534Ub"]')
        i = 0
        j = 1
        targets = []
        for result in results:
            target = {}
            if j > 1 and len(targets) < 1:
                break
            j += 1
            try:
                target['index'] = i
                target['text'] = result.find_element(By.CSS_SELECTOR, '.a9uirtCT').text
                i += 1
                if target['text'] == '':
                    i -= 1
                    continue
                else:
                    targets.append(target)

            except:
                continue
        filename = self.filename_comments + str(index) + '.json'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(json.dumps(targets, indent=2, ensure_ascii=False))
        driver.close()

    def main_heat(self):
        self.spider_heat()

    def main_comments(self):
        self.spider_heat()
        self.spider_comments()


if __name__ == '__main__':
    douyin = DouYinSpiderSelenium(datetime.now())
    douyin.main_heat()


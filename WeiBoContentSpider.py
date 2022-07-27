import json
import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime


class WeiBoSpiderComments:
    def __init__(self):
        self.driver = None

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

    def get_page(self, base_url, index):
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

    def main(self):
        self.open()
        self.login()
        filename = './WeiBo/WeiBo' + str(datetime.now().strftime("%d_%b_%Y")) + '.json'
        with open(filename, 'r', encoding='utf-8') as f:
            datas = json.loads(f.read())
        for data in datas:
            self.get_page(data['links'], data['index_s'])
        self.close()


if __name__ == "__main__":
    t1 = time.time()
    comment = WeiBoSpiderComments()
    comment.main()
    t2 = time.time()
    print(t2 - t1, 's')

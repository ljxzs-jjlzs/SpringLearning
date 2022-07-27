import json
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By



driver = webdriver.Chrome()
driver.maximize_window()

with open('./BiliBili/BiliBili25_Jul_2022.json', 'r', encoding='utf-8') as f:
    datas = json.loads(f.read())


for data in datas:
    link = data['link']
    driver.get(link)
    time.sleep(5)

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
    filename = './BiliBiliComment/comment' + str(data['index_s']) + '.json'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(json.dumps(targets, indent=2, ensure_ascii=False))

driver.close()

# driver.get('https://www.bilibili.com/video/BV1ZB4y1Y7Hm')
# time.sleep(5)
# i = 0
# # print('开始了')
# while i < 4:
#     driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
#     i += 1
#     time.sleep(5)
#
# results = driver.find_elements(By.CSS_SELECTOR, '.reply-item div[class="content-warp"]')
# i = 1
# targets = []
# for result in results:
#     target = {'index': i, 'text': result.find_element(By.CSS_SELECTOR, '.root-reply span').text}
#     # print(i)
#     i += 1
#     targets.append(target)
#     # print(result.find_element(By.CSS_SELECTOR, '.root-reply span').text)
# driver.close()
# with open("bilibil_comments.json", 'w', encoding='utf-8') as f:
#     f.write(json.dumps(targets, indent=2, ensure_ascii=False))

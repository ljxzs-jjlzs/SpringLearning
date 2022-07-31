import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import pyautogui

driver = webdriver.Chrome()
driver.maximize_window()
driver.get('https://www.zhihu.com/question/544969213?utm_division=hot_list_page')
time.sleep(3)
pyautogui.moveTo(1166, 787, duration=1)
time.sleep(2)
pyautogui.click()
pyautogui.moveTo(939, 630, duration=1)
time.sleep(2)
pyautogui.click()
time.sleep(5)


with open('./ZhiHu/ZhiHu25_Jul_2022.json', 'r', encoding='utf-8') as f:
    datas = json.loads(f.read())
for data in datas:
    link = data['links']
    driver.get(link)
    time.sleep(3)
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    time.sleep(5)
    pyautogui.moveTo(1912, 1016, duration=0.5)
    pyautogui.click()
    pyautogui.moveTo(1912, 500, duration=0.5)
    pyautogui.click()
    time.sleep(3)
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    time.sleep(5)
    items = driver.find_elements(By.CSS_SELECTOR, '.AnswerItem')

    targets = []
    for item in items:
        # print(item.get_attribute('class'))
        target = {
            'name': item.find_element(By.CSS_SELECTOR, 'div[class="AuthorInfo"] meta[itemprop="name"]').get_attribute(
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


driver.close()



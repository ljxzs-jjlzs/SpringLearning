import json
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By


def get_comment(url, number):
    targets = []
    driver = webdriver.Chrome()
    driver.get(url)
    driver.maximize_window()
    time.sleep(10)
    num_ = 1
    # for i in range(1, 3):
    items = driver.find_elements(By.CSS_SELECTOR, '.card-wrap div[class="card"]')
    for item in items:
        temp_item = item
        try:
            item = item.find_element(By.CSS_SELECTOR, '.card-feed div[node-type="like"]')
            target = {'name': item.find_element(By.CSS_SELECTOR, '.name').get_attribute('nick-name'),
                      'author_link': item.find_element(By.CSS_SELECTOR, '.name').get_attribute('href')}
        except:
            continue
        try:
            button = item.find_element(By.CSS_SELECTOR, 'a[action-type="fl_unfold"]')
            button_ = button.find_element(By.CSS_SELECTOR, '.wbicon')
            button_.click()
            time.sleep(2)
            target['content'] = item.find_element(By.CSS_SELECTOR, 'p[node-type="feed_list_content_full"]').text
        except:
            target['content'] = item.find_element(By.CSS_SELECTOR, '.txt').text
        button_ = temp_item.find_elements(By.CSS_SELECTOR, '.card-act ul li')
        target['forward'] = button_[0].text
        if button_[0].text == '转发':
            target['forward'] = '0'
        target['comment'] = button_[1].text
        if button_[1].text == '评论':
            target['comment'] = '0'
        target['like'] = button_[2].text
        if button_[2].text == '赞':
            target['like'] = '0'
        # button = button_[1].find_element(By.CSS_SELECTOR, 'a')
        # print(button.text)
        # button.click()
        print(num_)
        num_ += 1
        targets.append(target)
    time.sleep(5)

    driver.close()
    filename_ = './WeiBoComment/WeiBoComment' + str(number) + '.json'
    with open(filename_, 'w', encoding='utf-8') as f:
        f.write(json.dumps(targets, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    # t1 = time.time()
    # now = datetime.now()
    # now = str(now.strftime('%d_%b_%Y'))
    # filename = './WeiBo/WeiBo' + now + '.json'
    # with open(filename, 'r', encoding='utf-8') as f:
    #     datas = json.loads(f.read())
    # # datas = datas[8:]
    # # print(datas[0]['index_s'])
    # for data in datas:
    #     try:
    #         get_comment(data['links'], data['index_s'])
    #     except:
    #         continue
    #     time.sleep(2)
    # # get_comment('https://s.weibo.com/weibo?q=%E5%9A%A3%E5%BC%A0&Refer=top', 7)
    # t2 = time.time()
    # print('用时： ', t2 - t1)
    get_comment('https://s.weibo.com/weibo?q=%23%E6%B1%9F%E5%AE%8F%E6%9D%B0%E5%B7%B2%E8%81%94%E7%B3%BB%E4%B8%8A%E7%A6'
                '%8F%E5%8E%9F%E7%88%B1%23&Refer=top&page=%202&page=1', 51)
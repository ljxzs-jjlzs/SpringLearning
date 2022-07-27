import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import datetime

def get_page(url):
    browser = webdriver.Chrome()
    browser.get(url)
    time.sleep(2)
    results = browser.find_elements(By.CSS_SELECTOR, ".horizontal_1eKyQ")
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
        temp_target["index_s"] = temp_index.text
        target.append(temp_target)
    browser.close()
    return target


if __name__ == "__main__":
    url = "https://top.baidu.com/board?tab=realtime"
    results = get_page(url)
    today = datetime.today()
    now = today.strftime("%b_%d_%Y")
    filename = "./Baidu/Baidu" + str(now) + ".json"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(json.dumps(results, indent=2, ensure_ascii=False))

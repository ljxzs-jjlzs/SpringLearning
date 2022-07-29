import json

from selenium import webdriver
from selenium.webdriver.common.by import By


url = 'https://www.douyin.com/hot'
driver = webdriver.Chrome()
driver.get(url)
results = driver.find_elements(By.CSS_SELECTOR, '.BHgRhxNh')
print(len(results))
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
with open('DouyinHeat.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(targets, indent=2, ensure_ascii=False))


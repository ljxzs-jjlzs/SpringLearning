import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import pyautogui

driver = webdriver.Chrome()
t1 = time.time()
driver.maximize_window()
driver.get('https://www.zhihu.com/question/544969213?utm_division=hot_list_page')
# time.sleep(2)
time.sleep(3)
pyautogui.moveTo(1166, 787, duration=1)
time.sleep(2)
pyautogui.click()
pyautogui.moveTo(939, 630, duration=1)
time.sleep(2)
pyautogui.click()
time.sleep(5)
# i = 0
# # print('开始了')
# while i < 3:
#     driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
#     i += 1
#
#     time.sleep(3)


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
t2 = time.time()
print(t2-t1, '秒')
# import requests
#
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36',
#     'Host': 'www.zhihu.com',
#     'Cookie': '__snaker__id=cyjjvv3ltX3AXsV9; _zap=83df33c1-91a9-4f5a-b10a-9ae5ddb32a1d; d_c0="AJCfW3Mf5xKPTmgDxJaCeD2x38dxdZL_3qs=|1617528037"; _9755xjdesxxd_=32; YD00517437729195%3AWM_TID=%2BTjhzfh8HLNFQQFREUcqsBTBSkwCgzCP; _xsrf=3ZT1hqDzsE4njxCZO9gImICtsifc9doJ; __snaker__id=Oxl0YNk0UI51iKau; q_c1=8b70ced26567475d9b65d43c3308ae16|1657900370000|1657900370000; tst=h; NOT_UNREGISTER_WAITING=1; gdxidpyhxdE=3l%2FtXkWw0D%2FQ%2FJohV42XL5Nd4GnuTr%2FmEp7xW0kz7I4vcmyiG3LiNNSzlQyszrOsdjBkIh5B7P01yiYo6Y%2Bw1%5Cp%2Bf8mUfMwXh6Cumfb1AIqutRu%5CV3mpohNnWv7bef6GjEh6I%2BueoiLpEDWyurTD65HGM7HTVXYZsbQOrHGLw07EqHtG%3A1658552963334; YD00517437729195%3AWM_NIKE=9ca17ae2e6ffcda170e2e6eeb3ae349b8cff92b33c93eb8bb2d85f838a8ab0c14d83b288add94a98babbb4c72af0fea7c3b92a85acf9b1f543f49effa5f952b19e8393fb73878999b4e75aa399fea6f17ea891ab8af65eb89eb6b0e25cadeca18cae44f3f198b1bb73acae8ca2fb5baf97a187c83dacb4b9b7e65b81ae8296f76182a7a0d2e768a5aa9ca9c83987f0a0b2f76e97e9a1d3e734f1ef8890b33eb4afa789aa3482b0c091dc5ef68ca483f0669c979da6f237e2a3; YD00517437729195%3AWM_NI=Gt7PvI0B1DzZsBMrxyEWWSdRaG2ErvdOeiwVtBzOcPo4ok%2FH1%2FXP8yhrDAxQmIofE7hlwVgQCrNutkByP1dlgvTHE3E0PQtfU7o2d831Ho06pqih%2B8BpppYV6TlbmnXISEs%3D; captcha_ticket_v2=2|1:0|10:1658552153|17:captcha_ticket_v2|704:eyJ2YWxpZGF0ZSI6IkNOMzFfZW9OQS1OTHRWWWJxWnJkVzB6bVJJNzFoQ1hWSThOaVZLVkZJTzdWS2Q2YlBiLWlOSkp3RGRDY09DREE2U3Z2ME12RGQ2X0RiUVBXamx4dWlBQjZXa3JkOE5fWjBZZjJmLW9iNGJ0Vy1rcS0wVG4xUzA0SHhuVVI3WGpSMEU2YVRSVlptZDhXS29pd0pWRGVfaEk1VXFwSTJlWVQ3RDQ4em03VWNrS3RQLV9qTVd1N0pGcW1vYzBxc2tQMkFMcHlvekduZnAtbzYtY2N1LjlaLmE2LVVLZFM3MEE1QnNsYmZ3bUNBQ1JQUFRtQlNXRlBDTVhPZnhTN3dTMWRIR193eW1GUW1hQkxmSzZiS1NvcnZmMUFLWDRsTjBZOGU0MUFveXM0ZEU0emFXNmJCSXJpazJ2czB5NFZqQkVBcEdOQWJSNzdEY2FZMHlQMmJ3ZTRCMm9GbFREcHZGcEdlVVJ1elg5dk9vS093RnlJLXZ2dlVULUJKbW1BWTdNWTdDa0VPYkRhLWsyQ2J6SWtLMHh6aGViWW8yZ1dyVDl2b1JLbUpCRHhuR0xZYkZXakFJUmNhd05MUHc4Z2NaQmZzSnc4YjQwV0MuLjg0bE0uTHhnQW9NaTU0TmVEY0h6U2w5NlNXaWN5dVdZMXZlODh5b1BXMWU0SERYNU55dmVxMyJ9|ae47c7b6a21372d059d16e661798a7d6bec7dcfc3131af2201d07811cc7d6d49; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1658506215,1658534796,1658550166,1658552169; SESSIONID=aoAOlNqhLQh6dHKurwT8RIduDetarA0niSYoSqMgCU4; JOID=VV0dC00fk4sxjJsoFRJAWdVnnSAJfPHKcOHXVH1SwO4H5tJhbXnhXlyPlCUbBG285-7rBVQ3uPrUrfnTsrosBhE=; osd=UVEXAE0bn4E6jJ8kHxlAXdltliANcPvBcOXbXnZSxOIN7dJlYXPqXliDni4bAGG27O7vCV48uP7Yp_LTtrYmDRE=; captcha_session_v2=2|1:0|10:1658552171|18:captcha_session_v2|88:a0NGU2lsbEMxcWRpTWNseTBscEl4bVVEQTEvdnN0ZzFpZFk0di81UEd0YUUvYjRsNXVSaUo1QkVmQzJvaG94OQ==|315a3b438182746efef01997bf1bd5bb459f61317229692e93dfd0dc43f5c859; z_c0=2|1:0|10:1658552194|4:z_c0|92:Mi4xZFZKSEN3QUFBQUFBa0o5YmN4X25FaWNBQUFCZ0FsVk5nZ3dEWXdDUzZKeTZILTJTVG04Ri0yLVlxVHpzWS1yaUt3|f102677667fe46562c423e3115941ee863fdb255741872216ea0412cb0da6547; ariaDefaultTheme=undefined; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1658552287; KLBRSID=cdfcc1d45d024a211bb7144f66bda2cf|1658552291|1658552167'
#
# }
#
# response = requests.get('https://www.zhihu.com/question/544773680?utm_division=hot_list_page', headers=headers)
#
# print(response.status_code)
# print(response.text)



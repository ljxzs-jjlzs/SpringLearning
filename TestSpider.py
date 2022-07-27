import time

from BaiduSpiderFinal import BaiduSpider
from BiliBiliSpiderSelenium import BiliBiliSpider
from WeiBoSpiderSelenium import WeiBoSpider
from ZhihuSpiderSelenium import ZhiHuSpider
from datetime import datetime

if __name__ == "__main__":
    # now = str(datetime.now().strftime("%Y/%m/%d/%H:%M:%S"))
    now = datetime.now()
    t1 = time.time()
    baidu = BaiduSpider(now)
    baidu.main()
    print("百度爬取完毕！")
    bilibili = BiliBiliSpider(now)
    bilibili.main()
    print("B站爬取完毕！")
    weibo = WeiBoSpider(now)
    weibo.main()
    print("微博爬取完毕！")
    zhihu = ZhiHuSpider(now)
    zhihu.main()
    print("知乎爬取完毕！")
    t2 = time.time()
    print('用时： ', t2 - t1)
    # print(date.ctime())
    # print(datetime.now().strftime("%Y/%m/%d/%H:%M:%S"))



from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
import time
import pymysql.cursors
import datetime
import pytz
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt


# PhantomJSをSelenium経由で利用します.
des_cap = dict(DesiredCapabilities.PHANTOMJS)
des_cap['phantomjs.page.settings.userAgent'] = (
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) ' +
    'Chrome/28.0.1500.52 Safari/537.36'
)
#driver = webdriver.PhantomJS(desired_capabilities=des_cap, service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])
driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])

# PhantomJSで該当ページを取得＆レンダリングします
driver.get("https://suumo.jp/jj/bukken/ichiran/JJ010FJ001/?ar=030&bs=021&ta=13&jspIdFlg=patternShikugun&sc=13104&kb=1&kt=9999999&tb=0&tt=9999999&hb=0&ht=9999999&ekTjCd=&ekTjNm=&tj=0&cnb=0&cn=9999999")

# レンダリング結果をPhantomJSから取得します.
html = driver.page_source

# 画像のURLを取得する（JSでレンダリングしたところ）
bs = BeautifulSoup(html, "html.parser")
values = bs.find_all('div', class_ = 'dottable dottable--cassette')
tikunennsuu_array = []
nedan_array = []


#データベース周りの変数定義
conn = pymysql.connect(host='localhost',user='scrapist',db='scraping',password='password',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
try:
    with conn.cursor() as cursor:
        for value in values:
            dd  = value.find_all('dd')
            nedan = value.find('span', class_ = 'dottable-value')
            tikunensuu = dd[-1]
            nedan_int = nedan.text.replace('万円', '0000')
            nedan_int = nedan_int.replace('億', '')
            tikunennsuu_double = tikunensuu.text.replace('年', '.')
            tikunennsuu_double = tikunennsuu_double.replace('月', '')

            #INSERT文
            para = [tikunennsuu_double, nedan_int]
            sql_insert = "INSERT INTO suumo (chikunengetsu, hanbaikakaku) VALUES (%s, %s);"
            cursor.execute(sql_insert,para)
        
        #SELECT文
        sql_select = "SELECT*FROM suumo ORDER BY chikunengetsu ASC;"
        cursor.execute(sql_select)

        #SELECTした情報をfor文で表示する方法
        dbdata = cursor.fetchall()
        for row in dbdata:
            tikunennsuu_array.append(row['chikunengetsu'])
            nedan_array.append(row['hanbaikakaku'])

    conn.commit()
finally:
    #接続の終了
    conn.close()

#matplotlib関係
font = {"family":"IPAexGothic"}
matplotlib.rc('font', **font)
plt.figure(figsize=(20, 4))
plt.title('築年数と価格')
plt.xlabel('建築年[年]')
plt.ylabel('価格[円]')
plt.plot(tikunennsuu_array, nedan_array)
plt.savefig('./suumo.png')

# 終了
driver.quit()

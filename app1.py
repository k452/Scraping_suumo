import requests
from bs4 import BeautifulSoup
import pymysql.cursors
"""
#ページ読み込み
res = requests.get('https://fifaranking.net/ranking/')
soup = BeautifulSoup(res.content,'html.parser')

#大枠を取得
table = soup.find_all('table', class_ = 'table table-striped table-condensed')
tbody = soup.find_all('tbody')

#配列を用意
rank = []
country = []

#国名取得
for i in table:
    a = i.find_all('a')
    for j in a:
        country.append(j.text)
    
#順位取得
for i in tbody:
    tr = i.find_all('tr')
    for j in tr:
        k = j.find('td', class_ = '')
        if k != None:
            rank.append(k.text)
"""
#データベース周りの変数定義
conn = pymysql.connect(host='localhost',user='scrapist',db='scraping',password='password',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
try:
    with conn.cursor() as cursor:
        #INSERT文
        for i in range(len(rank)):
            para = [int(rank[i]), country[i]]
            sql = "INSERT INTO fifarank (rank, country) VALUES (%s, %s);"
            cursor.execute(sql,para)

        #CREATE文
            sql = "CREATE TABLE scraping.fifarank (rank int, country varchar(100));"
            cursor.execute(sql)
        
        #SELECT文
        sql = "SELECT*FROM fifarank;"
        cursor.execute(sql)

        #SELECTした情報をfor文で表示する方法
        dbdata = cursor.fetchall()
        for rows in dbdata:
            print(str(rows['rank']) + ':' + rows['country'])

    conn.commit()
finally:
    #接続の終了
    conn.close()


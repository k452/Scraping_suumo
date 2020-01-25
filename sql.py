import pymysql.cursors

conn = pymysql.connect(host='localhost',user='scrapist',db='scraping',password='password',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
try:
    with conn.cursor() as cursor:
        """    
        # 時刻取得
        now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
        time_init = str(now)
        time = time_init.split(".")[0]

        sql = "CREATE TABLE scraping.bitcoin (time timestamp, bid int, ask int, bidlev int, asklev int);"
        cursor.execute(sql)
    
        sql = "ALTER TABLE bitcoin MODIFY time DATETIME;"
        cursor.execute(sql)

        #INSERT文
        para = [time, int(value[0]), int(value[1]), int(value[2]), int(value[3])]
        sql_insert = "INSERT INTO bitcoin (time, bid, ask, bidlev, asklev) VALUES (%s, %s, %s, %s, %s);"
        cursor.execute(sql_insert,para)
        
        #SELECT文
        sql_select = "SELECT*FROM bitcoin;"
        cursor.execute(sql_select)

        #SELECTした情報をfor文で表示する方法
        dbdata = cursor.fetchall()
        for rows in dbdata:
            print(str(rows['time']) + ':' + str(rows['bid']) + '円:' + str(rows['ask']) + '円:' + str(rows['bidlev']) + '円:' + str(rows['asklev'])) + '円:'

        """

        sql = "CREATE TABLE scraping.suumo (chikunengetsu float, hanbaikakaku float);"
        cursor.execute(sql)
    conn.commit()
finally:
    #接続の終了
    conn.close()
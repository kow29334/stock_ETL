import requests, time ,random, os
from bs4 import BeautifulSoup
import pandas as pd



#===========================日期轉入測試開始============================================================

print('收盤日轉入測試開始')

date = str(time.strftime('%m/%d' , time.localtime())) #擷取本機今天日期


headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}

twse =['2303','3037','3576','2603','1314','1609','3481','2888','2353','2313','2887','1802','2409','9919','2368','2349','6443','5880','4142','2330','1101','2317',
'2609','6282','2885','6116','8046','2886','2880','2610','2891','2892','1444','3189','2881','2337','2890','3017','2448','2449','2882','3027','4906','2406','2363',
'2371','1589','2417','2344','2408']#50檔上市股票隨機抽取庫

tpex =['3105','3163','3218','3227','3260','3293','3324','3373','3374','3483','3540','3680','3691','4128','4743','4966','5347','5457','5474','5483','6104','6125',
'6223','6244','6462','6488','6510','6683','6732','8086']#30檔上櫃股票隨機抽取庫

stock_test = []#測試目標庫

rd_twse = random.choice(twse)#隨機抽測試上市收盤價轉入日期

stock_test.append(rd_twse)#加入測試目標庫

rd_tpex = random.choice(tpex)#隨機抽測試上櫃收盤價轉入日期

stock_test.append(rd_tpex)#加入測試目標庫

test_list =[] #上市櫃收盤轉入日期庫

for s in stock_test:
    print('測試 %s 股票' % s )

    url = 'https://goodinfo.tw/StockInfo/StockDetail.asp?STOCK_ID=%s' % s

    # proxies = {#'https': '118.163.83.21:3128',
    #            #'http': '219.121.1.93:3128',
    #            #'https': '59.124.224.180:3128',
    #            #'http': '159.203.2.130:80',
    #            'http': '83.96.237.121:80',
    #            'https': '151.80.148.71:3128',
    #            #'http': '91.205.174.26:80',
    #            #'https': '167.99.144.242:8888'
    #            }

    ss = requests.session()

    res = ss.get(url=url, headers=headers)#, proxies=proxies)

    res.encoding = 'utf-8'

    soup = BeautifulSoup(res.text, 'html.parser')

    #print('Request IP:',proxies)

    test = soup.select('table[class="solid_1_padding_3_1_tbl"]')[0]

    test1 = test.select('table[class="none_tbl"]')[0].text

    test_str = str(test1).strip().split(' ')[1]

    test_list.append(test_str)

    y = random.randint(15, 60)  # 爬完一檔股票隨機休息15~60秒

    time.sleep(y)

    print('休息', y, '秒')  # 印出休息秒數


count = 0

for st in test_list:
    if st == date:
        count += 1

print('上市與上櫃共 %d 個轉入' % count)
print('收盤日轉入測試結束')

print('======================================================================================================================================')


#=======================================================日期轉入測試結束=======================================================================

#=======================================================擷取大盤收盤五價=======================================================================


df = pd.DataFrame(columns=['漲跌價', '成交量', '漲跌幅', '開盤價', '最高價', '最低價', '收盤價'])

if count == 2:
    print('擷取台北股市大盤收盤價開始，請耐心等候')

    # proxies = {#'http':'168.169.96.14:8080',
    #             #'https':'168.169.96.2:8080',
    #            'http':'185.134.23.197:80',
    #            'https':'64.235.204.107:8080'
    #            }

    tai_dict = {'twse':'https://goodinfo.tw/StockInfo/StockIdxDetail.asp?STOCK_ID=%E5%8A%A0%E6%AC%8A%E6%8C%87%E6%95%B8',
                'tpex':'https://goodinfo.tw/StockInfo/StockIdxDetail.asp?STOCK_ID=%E6%AB%83%E8%B2%B7%E6%8C%87%E6%95%B8'}

    for c in tai_dict:

        print('擷取 %s 收盤價開始' % c)

        tai_url = '%s ' % tai_dict[c]

        ss = requests.session()

        res = ss.get(url=tai_url, headers=headers)#, proxies=proxies, timeout = 6)

        #print('Request IP:',proxies)

        res.encoding = 'utf-8' #設定編碼

        soup_tai = BeautifulSoup(res.text, 'html.parser')

        tai = soup_tai.select('tr[valign="top"]')[0]

        tai1 = tai.select('table[class="solid_1_padding_4_2_tbl"]')[1].text

        tai1_str = str(tai1).strip().split(' ')

        price = tai1_str[6]

        Rising_and_falling_prices = tai1_str[7]

        per0 = tai1_str[8]

        per = per0.split('%')[0]

        open = tai1_str[9]

        hight = tai1_str[10]

        low = tai1_str[11]

        Volume = tai1_str[20]

        tai_data = [Rising_and_falling_prices, Volume, per, open, hight, low, price]

        df.loc[c] = tai_data

        y = random.randint(15, 60)  # 爬完一檔股票隨機休息15~60秒

        time.sleep(y)

        print('休息', y, '秒')  # 印出休息秒數

        print('收盤價擷取完畢')

        print(
            '------------------------------------------------------------------------------------------------------------------------------------')

    print('擷取台北股市大盤收盤價完畢')

    print('======================================================================================================================================')

# =========================================================擷取大盤收盤五價結束==================================================================

# =========================================================擷取個股收盤五價=====================================================================

    stock = ['2834', '1702', '2324', '2377', '3576', '8069', '2354', '2881', '2317', '2419', '2313', '3144', '2330',
             '6173', '006206', '2014', '1314', '8049', '8110', '0050', '2405', '2353', '2880', '0056', '2884', '8046',
             '1522', '4919', '2449', '2520', '5439']

    stock_count = int(len(stock))

    print('擷取收盤價開始，總共 %d檔股票需擷取請耐心等候' % stock_count)

    for i in stock:
        print('擷取 %s 檔股票' % i)

        # proxies = {#'https': '118.163.83.21:3128',
        #            #'http': '219.121.1.93:3128',
        #            #'https': '59.124.224.180:3128',
        #            #'http': '159.203.2.130:80',
        #            'http': '83.96.237.121:80',
        #            'https': '151.80.148.71:3128',
        #            #'http': '91.205.174.26:80',
        #            #'https': '167.99.144.242:8888'
        #            }


        url = 'https://goodinfo.tw/StockInfo/StockDetail.asp?STOCK_ID=%s' % i

        ss = requests.session()

        res = ss.get(url=url, headers=headers)#, proxies=proxies)

        #print('Request IP:', proxies)

        res.encoding = 'utf-8'

        soup = BeautifulSoup(res.text, 'html.parser')

        stock = soup.select('table[class="solid_1_padding_3_1_tbl"]')[0]

        stock1 = stock.select('tr[align="center"]')[0].text

        stock_title1 = str(stock1).strip().split(' ')

        stock2 = stock.select('tr[align="center"]')[1].text

        sotck2_str = str(stock2).strip().split(' ')

        stock3 = stock.select('tr[align="center"]')[2].text

        sotck3_str = str(stock3).strip().split(' ')

        stock4 = stock.select('tr[align="center"]')[3]

        stock5 = stock4.select('td')[0].text

        price = sotck2_str[0]

        Rising_and_falling_prices = sotck2_str[2]

        per0 = sotck2_str[3]

        per = per0.split('%')[0]

        open = sotck2_str[5]

        hight = sotck2_str[6]

        low = sotck2_str[7]

        Volume = str(stock5)

        stock_title = [stock_title1[2], sotck3_str[0], stock_title1[3], stock_title1[5], stock_title1[6],
                        stock_title1[7], stock_title1[0]]

        stock_data = [Rising_and_falling_prices, Volume, per, open, hight, low, price]

        df.loc[i] = stock_data

        stock_count -= 1

        y = random.randint(20, 60)  # 爬完一檔股票隨機休息20~60秒

        time.sleep(y)

        print('休息', y, '秒')  # 印出休息秒數

        print('擷取完畢，剩下 %d 檔未擷取' % stock_count)

        print(
            '------------------------------------------------------------------------------------------------------------------------------------')

    print('擷取個股收盤價完畢')

    print(
        '======================================================================================================================================')

if count != 2 :

    information = '收盤價尚未轉入(上市或上櫃價格其一尚未轉入請稍等再試)'

    df.loc[0] = information

    print(information)#上市或上櫃價格其一尚未轉入請稍等在試

    print('======================================================================================================================================')

#=========================================================擷取個股收盤五價結束=====================================================================

#=============================================================存檔================================================================================

print('儲存檔案開始')

folder = './twstock'

if not os.path.exists(folder):

    os.mkdir(folder)

loc_time = time.localtime()

time = time.strftime('%Y%m%d', loc_time)

path = './twstock/%s.csv' % time

df.to_csv(path, index=True, encoding='utf-8')

print('儲存檔案結束')

print('======================================================================================================================================')
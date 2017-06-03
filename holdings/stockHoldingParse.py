import datetime
import urllib.request
from bs4 import BeautifulSoup
from holdings.stockHoldingsResult import HoldingsResult
import sys

def getNewHoldings (stockCode):
    url = 'http://quotes.money.163.com/f10/nbcg_' + stockCode + '.html'
    try:
        content = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(content)
        tables = soup.findAll("table", {'class':'table_bg001 border_box limit_sale'})
        if tables == None or len(tables) == 0:
            return None

        table = tables[1]
        soupTable = BeautifulSoup(str(table))
        list = soupTable.find_all("tr")

        if (len(list) == 1):
            return None

        result = getLastMonthHoldings(stockCode, str(list[1:]))
        if result == None or result.holding == "":
            return None

        return result

    except Exception as e:
        reason = "[%s]-----"%stockCode + str(e) + "    " + sys._getframe().f_code.co_filename + ":" + str(sys._getframe().f_lineno)
        print(reason)
        return None
    return None


def getLastMonthHoldings(code, holdings):
    soup = BeautifulSoup(holdings)
    list = soup.find_all("tr")
    holding = ""
    reason = ""
    num = ""
    price = ""
    money = 0
    line = 0
    for i in range(len(list)):
        item = list[i]

        if str(item).__contains__("暂无数据"):
            return None

        soupChild = BeautifulSoup(str(item))
        temp = soupChild.findAll("td")

        #减持的就不看了
        if ((float)(temp[4].string)) <= 0:
            continue

        #抓取一个月内的数据,相信数据是排序的，need fixme?
        if False == isInOneMonth(temp[2].string):
            break

        if line != 0:
            holding = holding + '''</br>'''
            reason = reason + '''</br>'''
            num = num + '''</br>'''
            price = price + '''</br>'''
        holding = holding + temp[0].string + ", " + temp[1].string + ", " + temp[2].string
        num = num + temp[4].string
        price = price + temp[5].string
        reason = reason + temp[3].string
        try:
            money = money + float(temp[5].string) * float(temp[4].string)
        except:
            money = 0
        line = line + 1

    if money == 0:
        moneyString = "--"
    else:
        moneyString = "%.2f"%money
    return HoldingsResult(code, holding, num, price, moneyString, reason, False)

def isInOneMonth(time):
    dt = datetime.datetime.strptime(time, "%Y-%m-%d")
    now = datetime.datetime.now()
    sevenDays = datetime.timedelta(days=90)
    if now - dt > sevenDays:
        return False
    return True

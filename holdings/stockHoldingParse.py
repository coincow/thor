import datetime
import urllib.request

from bs4 import BeautifulSoup

from holdings.stockHoldingsResult import HoldingsResult


def getNewHoldings (stockCode):
    url = 'http://quotes.money.163.com/f10/nbcg_' + stockCode + '.html'
    try:
        content = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(content)
        table = soup.find("table", {'class':'table_bg001 border_box limit_sale'})

        soupTable = BeautifulSoup(str(table))
        list = soupTable.find_all("tr")

        if (len(list) == 1):
            return None

        result = getLastWeekHoldings(stockCode, str(list[1:]))
        if result == None or result.holding == "":
            return None

        return result

    except Exception as e:
        print(e)
        return None
    return None


def getLastWeekHoldings(code, holdings):
    soup = BeautifulSoup(holdings)
    list = soup.find_all("tr")
    holding = ""
    for i in range(0, len(list)):
        item = list[i]

        if str(item).__contains__("暂无数据"):
            return None

        soupChild = BeautifulSoup(str(item))
        temp = soupChild.findAll("td")

        if False == isInOneMonth(temp[3].string):
            continue

        if i != 0:
            holding = holding + '''</br>'''
        holding = holding + temp[0].string + ", " + temp[1].string + ", " + temp[2].string + ", " + temp[3].string

    return HoldingsResult(code, holding, "", False)

def isInOneMonth(time):
    dt = datetime.datetime.strptime(time, "%Y-%m-%d")
    now = datetime.datetime.now()
    sevenDays = datetime.timedelta(days=30)
    if now - dt > sevenDays:
        return False
    return True

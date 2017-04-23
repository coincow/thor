import urllib
from bs4 import BeautifulSoup

from holdings.stockMarginResult import MarginResult

def getMargin(stockCode):

    if stockCode[0] == '6':
        stockCode = str(stockCode).zfill(7)
    else:
        stockCode = '1' + str(stockCode).zfill(6)

    url = 'http://quotes.money.163.com/' + stockCode + '.html'
    try:
        content = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(content)
        tables = soup.findAll("div", {'class': 'inner_box fund_merge'})
        if tables == None or len(tables) == 0:
            return None

        soupTable = BeautifulSoup(str(tables))
        list = soupTable.find_all("tr")
        if (len(list) <= 2):
            return None

        result = getLastWeekMargin(stockCode, list[2:])

    except:
        return None


    return result


def getLastWeekMargin(code, list):

    endIndex = 0
    startIndex = len(list) - 1

    soupChild = BeautifulSoup(str(list[startIndex]))
    start = soupChild.findAll("td")
    soupChild = BeautifulSoup(str(list[endIndex]))
    end = soupChild.findAll("td")

    try:
        buy = round(float((end[3].string).replace(',', '.')) - float((start[3].string).replace(',', '.')), 2)
        balance = round(float((end[8].string).replace(',', '.')), 2)
        percent = round(buy/balance, 2)*100
    except:
        return None

    return MarginResult(code[1:], buy, balance, percent, False)



import urllib.request
from bs4 import BeautifulSoup

def getNewHoldings (stockCode):
    stockCode = stockCode[1:]
    url = 'http://quotes.money.163.com/f10/nbcg_' + stockCode + '.html'
    try:
        content = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(content)
        table = soup.find("table", {'class':'table_bg001 border_box limit_sale'})

        soupTable = BeautifulSoup(str(table))
        list = soupTable.find_all("tr")

        if (len(list) == 1):
            return ""

        return str(list[1:])

    except Exception as e:
        print(e)
        return ""
    return ""
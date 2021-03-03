import re

from pdfplumber import PDF

from stocks import *
import utils.financial as uf

positionPattern = re.compile(r'(.*)\s+(\d*\.?\d+\sStk\.)\s+(-?\d+,\d+\s\w+)\s+(-?\d*\.?\d+,\d+\s\w+)')
amountPattern = re.compile(r'(\d+)\sStk\.')
priceCurrencyPattern = re.compile(r'(-?\d*\.?\d+,\d+)\s(\w+)')
isinPattern = re.compile(r'([A-Z]{2}[A-Z0-9]{10})')
datePattern = re.compile(r'([0-3][0-9][/.][0-3][0-9][/.](?:[0-9][0-9])?[0-9][0-9])')


def analyze_buy(pdf: PDF):
    global price
    valuta_line = -1
    stock_trade = StockTrade
    for line in pdf.pages[0].extract_text().split("\n"):
        # print("OOPS! I bought something :)")
        lower = line.lower()
        if lower.__contains__("stk."):
            m = positionPattern.search(line)
            product = m.group(1)
            g2 = m.group(2)
            amount = int(amountPattern.match(g2).group(1))
            market_price = m.group(3)
            m3 = priceCurrencyPattern.match(market_price)
            price = Price(Money(uf.comma_decimal2float(m3.group(1)), m3.group(2)), None)
            sum_price = m.group(4)
            m4 = priceCurrencyPattern.match(sum_price)
            sum_price_value = uf.dot_decimal2float(m4.group(1))
            sum_price_currency = m4.group(2)
        if lower.__contains__("isin: "):
            isin = isinPattern.search(line).group(1)
        if lower.__contains__("fremdkostenzuschlag"):
            m = priceCurrencyPattern.search(line)
            cost = Price(Money(uf.comma_decimal2float(m3.group(1)), m.group(2)), None)
        if lower.__contains__("valuta"):
            valuta_line = 2
        if valuta_line > 0:
            valuta_line -= valuta_line
            continue
        if valuta_line == 0:
            valuta_line -= 1
            m = datePattern.search(line)
            valuta_string = m.group(0)
            valutas = valuta_string.split('.')
            valuta = date(int(valutas[2]), int(valutas[1]), int(valutas[0]))
            m = priceCurrencyPattern.search(line)
            if m.group(0)[0].isdigit():
                kind = Trade.SELL
            elif m.group(0)[0] == '-':
                kind = Trade.BUY
            else:
                kind = Trade.UNKNOWN

    stock_trade.stock = Stock(isin, product)
    stock_trade.price_per_unit = price
    stock_trade.amount = amount
    stock_trade.valuta = valuta
    stock_trade.cost = cost
    stock_trade.kind = kind
    return StockTrade


def analyze_pretax(pdf: PDF):
    pass


def analyze_dividend(pdf: PDF):
    pass


def analyze(pdf: PDF):
    text = pdf.pages[0].extract_text()
    if text.__contains__("WERTPAPIERABRECHNUNG"):
        return analyze_buy(pdf)
    if text.__contains__("DEVIDENDE"):
        return analyze_dividend(pdf)
    if text.__contains__("VORABPAUSCHALE"):
        return analyze_pretax(pdf)

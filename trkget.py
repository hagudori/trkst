import jsm
import datetime
import time
import csv
import pandas as pd


def price_to_csv(code, price):
    """PriceデータをCSV出力用フォーマットに変換"""
    return [code, price.date.strftime("%Y/%#m/%#d"),
            price.open, price.high, price.low, price.close,
            price.volume, price._adj_close]


if __name__ == "__main__":
    out_file = "etf\\ETF_Stock_Prices_Daily.csv"
    c = csv.writer(open(out_file, "a"))
    c.writerow(["stock_code", "date", "open", "high", "low",
                "close", "volume", "adj_close"])

    # データ取得期間（最大）
    start_date = datetime.date(2005, 9, 1)
    end_date = datetime.date(2017, 5, 11)

    df = pd.read_csv("etf\\ETF_list.csv")
    stock_list = df["stock_code"]

    for stock_code in stock_list:
        time.sleep(10)

        print(stock_code)

        try:
            q = jsm.Quotes()
            historical_prices = q.get_historical_prices(
                stock_code, jsm.DAILY, start_date=start_date,
                end_date=end_date)
            for price in historical_prices:
                c.writerow(price_to_csv(stock_code, price))

        except:
            pass
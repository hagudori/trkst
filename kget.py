"""
銘柄データ・ETFデータをWEBページから取得・整形する
"""
# ----- Import Libraries ---------------------------------------------
import pandas as pd
import datetime
import codecs
import math
import csv
import time
import kjson
from dateutil.relativedelta import relativedelta
from dateutil.rrule import *

# ----- Setting Parameters -------------------------------------------
GET_MONTH = 13  # 過去何カ月分のデータを取得するか指定(ETFのみ)
JOIN_DATE = False   # 結合時、ETFごとに日付を出力するかどうか
JOIN_DIFF = True    # 結合時、ETFごとに前日比を出力するかどうか
DIR_ETF_DATA = "etf\\"  # ETFデータディレクトリ
DIR_CODE_DATA = "code\\"    # 銘柄データディレクトリ
DIR_JOIN_DATA = "code_join\\"   # 結合データディレクトリ


# ----- Definition of Local and External Function --------------------
def get_etf():
    """指定カ月分の過去のETFデータを取得（スクレイピングする）"""

    # ETF情報を取得
    etf_list = kjson.read_etf()

    # 前日の日付
    day_end = datetime.datetime.now() - datetime.timedelta(days=1)

    # 指定カ月前の日付
    day_start = day_end - relativedelta(months=GET_MONTH)

    # 土日を除く日数を計算(本当は、祝日を除いた営業日数がいいのだが)
    weekday = len(list(rrule(DAILY, byweekday=(MO, TU, WE, TH, FR),
                             dtstart=day_start, until=day_end)))

    # ページ数を計算(厳密に正確ではない)
    page = int(math.ceil(weekday) / 20)

    # ETFごとにループ
    for dic in etf_list:

        # URLを設定(範囲日付)
        url_base = "https://info.finance.yahoo.co.jp/history/?"
        url_base = url_base + "code=" + dic["code"] + ".T"
        url_base = url_base + \
            "&sy=" + str(day_start.year) + \
            "&sm=" + str(day_start.month) + \
            "&sd=" + str(day_start.day) + \
            "&ey=" + str(day_end.year) + \
            "&em=" + str(day_end.month) + \
            "&ed=" + str(day_end.day) + \
            "&tm=d"

        # データ初期化
        result = pd.DataFrame()

        # 1ページずつ取得
        for i in range(1, page + 1):

            # URLを設定(ページ)
            if i == 1:
                url = url_base
            else:
                url = url_base + "&p=" + str(i)

            # URL内の表を取得
            frames = pd.read_html(url)

            # DataFrameに変換
            df = pd.DataFrame(frames[1])

            # ヘッダを削除
            df = df.drop(0)

            # データを結合
            result = pd.concat([result, df])

            # yahooサーバへの負荷軽減のため、1秒待機
            time.sleep(1)

        # PATHを設定
        path = DIR_ETF_DATA + "etf_" + dic["code"] + ".csv"

        # CSVに吐き出し
        result.to_csv(path)

        # CSVの行列ヘッダを削除
        data = []
        with open(path, "r") as f:
            reader = csv.reader(f, delimiter=",")
            next(reader)   # 1行目を飛ばす
            for row in reader:
                row.pop(0)  # 1列目を削除
                date = datetime.datetime.strptime(row[0], "%Y年%m月%d日")
                row[0] = date.strftime("%Y/%#m/%#d")  # フォーマット変換
                data.append(row)    # リストに追加
        with open(path, "w") as f:
            writer = csv.writer(f, delimiter=",", lineterminator="\n")
            writer.writerows(data)   # リストを書込み

        # 途中経過を出力
        print("CSV create complete! ", dic["code"])


def get_code():
    """銘柄データを取得（スクレイピング）する　期間は250日固定"""

    # 銘柄情報を取得
    code_list = kjson.read_code()

    # 銘柄ごとにループ
    for code in code_list:

        # URLを設定
        url = "http://k-db.com/stocks/" + code["code"] + "-T"

        # URL内の表を取得
        frames = pd.read_html(url)

        # DataFrameに変換
        df = pd.DataFrame(frames[0])
        del df[1], df[8]  # 不要列を削除
        # 列名を変更
        df.rename(columns={0: "Date", 2: "Open", 3: "High", 4: "Low",
                           5: "Close", 6: "Volume",
                           7: "Trading Value"},
                  inplace=True)

        # PATHを設定
        path = DIR_CODE_DATA + "code_" + code["code"] + ".csv"

        # CSVに吐き出し
        df.to_csv(path)

        # CSVを整形
        data = []
        with open(path, "r") as f:
            reader = csv.reader(f, delimiter=",")
            next(reader)
            for row in reader:
                row.pop(0)  # 1列目を削除
                date = datetime.datetime.strptime(row[0], "%Y-%m-%d")
                row[0] = date.strftime("%Y/%#m/%#d")  # フォーマット変換
                data.append(row)  # リストに追加
        with open(path, "w") as f:
            # ヘッダ行を挿入
            data.insert(0, ["Date", "Open", "High", "Low",
                            "Close", "Volume", "Trading Value"])
            writer = csv.writer(f, delimiter=",", lineterminator="\n")
            writer.writerows(data)  # リストを書込み

        # 途中経過を出力
        print("CSV create complete! ", code["code"])


def join_etf_code():
    """銘柄データに、ETFデータを結合する"""

    # ETF情報を取得
    etf_list = kjson.read_etf()

    # 銘柄情報を取得
    code_list = kjson.read_code()

    # 銘柄ごとにループ
    for code in code_list:

        # 銘柄データを読込
        df_code = pd.read_csv(DIR_CODE_DATA + "code_" +
                              code["code"] + ".csv", header=0)
        df_code.columns = ["Date", "Open", "High", "Low",
                           "Close", "Volume", "Trading Value"]
        df_code["index"] = [i for i in range(len(df_code))]

        # ETFごとにループ
        for etf in etf_list:

            # ETFデータを操作
            with codecs.open(DIR_ETF_DATA + "etf_" + etf["code"] +
                             ".csv", "r", "Shift-JIS",
                             "ignore") as file:

                # ETFデータを取得
                df_etf = pd.read_table(file, delimiter=",",
                                       names=("Date", "Open", "High",
                                              "Low", "Close",
                                              "Volume",
                                              "Trading Value"))
                # 初期化
                dates = []
                closes = []
                close_back = pd.Series()

                # 銘柄データの日付ループ
                for d in df_code["Date"]:

                    # ETFデータで、該当する日付を抽出
                    date = df_etf.loc[(df_etf.Date == d), "Date"]

                    # 該当の日付が存在する場合
                    if len(date) != 0:
                        # 日付を追加
                        dates.append(date.values[0])
                        # 終値を抽出
                        close = df_etf.loc[
                            (df_etf.Date == d), "Close"]
                        # 終値を追加
                        closes.append(close.values[0])
                        close_back = close

                    # 該当の日付が存在しない場合
                    else:
                        # 日付を追加
                        dates.append(d)
                        # 前回日の終値を抽出(30日過去まで遡る)
                        date_ = datetime.datetime.strptime(d,
                                                           "%Y/%m/%d")
                        for i in range(1, 31):
                            date_old = date_ - datetime.timedelta(
                                days=i)
                            date_str = date_old.strftime("%Y/%#m/%#d")
                            close = \
                                df_etf[
                                    df_etf["Date"] == date_str].Close
                            if len(close) != 0:
                                break
                            if i == 31 - 1:
                                # 30日過去にもデータがない場合、前回読込値を
                                # 使用する（未来のデータとなってしまうが）
                                close = close_back
                        # 終値を追加
                        closes.append(close.values[0])
                        close_back = close

                # ETFの日付と終値のDataFrameを生成
                if JOIN_DATE:
                    df_etf2 = pd.DataFrame(
                        {"Date_" + str(etf["code"]): dates,
                         "Close_" + str(etf["code"]): closes})
                else:
                    df_etf2 = pd.DataFrame(
                        {"Close_" + str(etf["code"]): closes})

                # 銘柄データに結合
                df_code = pd.concat([df_code, df_etf2], axis=1)

                # 前日比を生成
                if JOIN_DIFF:
                    df_code["diff_" + str(etf["code"])] = \
                        df_code["Close_" + str(etf["code"])] / \
                        df_code["Close_" + str(etf["code"])].shift(
                            -1) - 1

        # 結合結果を出力
        df_code.to_csv(
            DIR_JOIN_DATA + "code_" + code["code"] + "_join.csv")

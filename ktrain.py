"""
モデル学習を行う
"""
# ----- Import Libraries ---------------------------------------------
import pandas as pd
import kjson
import kget
from sklearn.ensemble import RandomForestClassifier

# ----- Setting Parameters -------------------------------------------


# ----- Definition of Local and External Function --------------------
def train_random_forest():
    """
    ランダムフォレストを使用した株価予測
    
    過去250日分のデータをもとに、上げ下げ(1 or -1)を予測する
    """

    print("----- train_random_forest Start -----")

    # ETF情報を取得
    etf_list = kjson.read_etf()

    # 銘柄情報を取得
    code_list = kjson.read_code()

    # 説明変数のリスト(ETFの前日比)を生成
    x_list = []
    for etf in etf_list:
        x_list.append("diff_" + etf["code"])

    # 銘柄ごとにループ
    for code in code_list:

        # 銘柄データを読込
        df = pd.read_csv(kget.DIR_JOIN_DATA + "code_" +
                         code["code"] + "_join.csv")
        df = df.sort_values(by=["index"], ascending=False)
        df = df.iloc[0:len(df) - 1]

        # トレーニングデータ(最新と最古データを除く全データ)
        df_train = df.iloc[1: len(df) - 1]

        # テストデータ(最新データ)
        df_test = df.iloc[len(df) - 1: len(df)]

        # 学習データの生成
        x_train = []
        y_train = []
        for s in range(0, len(df_train) - 1):

            # 説明変数のデータを追加
            x_train.append(df_train[x_list].iloc[s])

            # 前日終値との騰落を目的変数に追加
            if df_train["Close"].iloc[s + 1] > \
                    df_train["Close"].iloc[s]:
                y_train.append(1)
            else:
                y_train.append(-1)

        # ランダムフォレストを構築
        rf = RandomForestClassifier(n_estimators=len(x_train),
                                    random_state=0)
        # 学習
        rf.fit(x_train, y_train)

        # テストデータ
        x_test = df_test[x_list].iloc[0]

        # 予測
        y_test = rf.predict(x_test.values.reshape(1, -1))

        # 予測結果を出力する
        print(code["code"], " : ", code["name"], " -> ", y_test[0])

        # 各銘柄における、説明変数(ETF)の重要度を出力する
        print(rf.feature_importances_)

    print("----- train_random_forest End -----")

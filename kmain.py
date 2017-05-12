import kget
import kjson
import ktrain

# Jsonファイルを更新
# kjson.write_etf()
# kjson.write_code()
# print("----- Json File Update End -----")

# 最新ETFデータを取得
# kget.get_etf()
# print("----- ETF Data Update End -----")

# 最新銘柄データを取得
# kget.get_code()
# print("----- Code Data Update End -----")

# 銘柄データにETFデータを結合
kget.join_etf_code()
# print("----- Data Join End -----")

ktrain.train_random_forest()

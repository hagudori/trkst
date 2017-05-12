"""
銘柄データ・ETFデータをJsonに書込・読込する
"""
# ----- Import Libraries ---------------------------------------------
import json
import codecs

# ----- Setting Parameters -------------------------------------------
FILE_NAME_CODE_JSON = "inf\\code_list.json"     # 銘柄情報ファイル名
FILE_NAME_ETF_JSON = "inf\\etf_list.json"   # ETF情報ファイル名


# 各リスト変更後は、本スクリプトを実行して、Jsonを更新する
# 銘柄リスト定義
code_list = [
    {"code": "4307", "name": "野村総合研究所"},
    {"code": "4324", "name": "電通"},
    {"code": "4321", "name": "ケネディクス"},

]

# ETFリスト定義
etf_list = [
    {"code": "1309", "name": "上海株式指数・上証50連動型上場投資信託"},
    {"code": "1313", "name": "サムスンKODEX200証券上場指数投資信託"},
    {"code": "1314", "name": "上場インデックスファンドS&P日本新興株100"},
    {"code": "1322", "name": "上場インデックスファンド中国A株（パンダ）CSI300"},
    {"code": "1326", "name": "SPDRゴールド・シェア"},
    {"code": "1343", "name": "NEXT FUNDS 東証REIT指数連動型上場投信"},
    {"code": "1543", "name": "純パラジウム上場信託（現物国内保管型）"},
    {"code": "1548", "name": "上場インデックスファンド中国H株（ハンセン中国企業株）"},
    {"code": "1549", "name": "上場インデックスファンドNifty50先物（インド株式）"},
    {"code": "1551", "name": "JASDAQ-TOP20上場投信"},
    {"code": "1633", "name": "NEXT FUNDS 不動産（TOPIX-17）上場投信"},
    {"code": "1673", "name": "ETFS 銀上場投資信託"},
    {"code": "1678", "name": "NEXT FUNDS インド株式指数・Nifty 50連動型上場投信"},
    {"code": "1681", "name": "上場インデックスファンド海外新興国株式（MSCIエマージング）"},
    {"code": "1682", "name": "NEXT FUNDS 日経・東商取白金指数連動型上場投信"},
    {"code": "1698", "name": "上場インデックスファンド日本高配当（東証配当フォーカス100）"},
    {"code": "1626", "name": "NEXT FUNDS 情報通信･サービス上場投信"},
]


# ----- Definition of Local and External Function --------------------
def write_code():
    """銘柄リストデータをjsonに書き込む"""
    fw = codecs.open(FILE_NAME_CODE_JSON, "w", "utf-8")
    json.dump(code_list, fw, indent=4, ensure_ascii=False)
    fw.close()


def read_code():
    """銘柄リストデータをjsonから読み込む"""
    fr = codecs.open(FILE_NAME_CODE_JSON, "r", "utf-8")
    ret_list = json.load(fr)
    fr.close()
    return ret_list


def write_etf():
    """ETFリストデータをjsonに書き込む"""
    fw = codecs.open(FILE_NAME_ETF_JSON, "w", "utf-8")
    json.dump(etf_list, fw, indent=4, ensure_ascii=False)
    fw.close()


def read_etf():
    """ETFリストデータをjsonから読み込む"""
    fr = codecs.open(FILE_NAME_ETF_JSON, "r", "utf-8")
    ret_list = json.load(fr)
    fr.close()
    return ret_list


# ----- Main Program -------------------------------------------------
if __name__ == "__main__":
    write_code()
    write_etf()

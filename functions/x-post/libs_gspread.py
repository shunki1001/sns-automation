# %%
import datetime
from datetime import datetime, timedelta

import gspread
import pandas as pd
import pytz
from oauth2client.service_account import ServiceAccountCredentials

tz_tokyo = pytz.timezone("Asia/Tokyo")
today_tokyo = datetime.now(tz_tokyo).replace(hour=0, minute=0, second=0, microsecond=0)

# Google Sheets APIとGoogle Drive APIのスコープを定義
scope = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
]

# サービスアカウントのJSONファイルで認証
creds = ServiceAccountCredentials.from_json_keyfile_name(
    "./smarthome-428311-06335f16edbf.json",
    scope,
)
gc = gspread.authorize(creds)


def get_coupon_gspread_data() -> pd.DataFrame:

    # シート名で指定してスプレッドシートを開く
    workbook = gc.open_by_key("1_biAFUmsFz88ncmwDexwVX-sXdQKgWiPoIWjO0zlC6o")
    worksheet = workbook.worksheet("商品管理")

    # シート内の全データを取得（リストのリストになる）
    data = worksheet.get_all_values()

    # 1行目をヘッダーとしてpandasのDataFrameに変換
    df = pd.DataFrame(data[1:], columns=data[0])

    return _clean_coupon_df(df)


def _clean_coupon_df(df: pd.DataFrame) -> pd.DataFrame:
    # 必要なカラムだけ抽出（例として start_at, end_at, flag のみ）
    selected_columns = [
        {"spread": "投稿文", "df": "content"},
    ]
    spread_columns = [col_map["spread"] for col_map in selected_columns]

    # 2. リネーム用の辞書を作成
    rename_mapping = {col_map["spread"]: col_map["df"] for col_map in selected_columns}

    # 3. DataFrameから必要なカラムを抽出し、その上でカラム名をrename
    df_selected = df[spread_columns].rename(columns=rename_mapping)

    return df_selected

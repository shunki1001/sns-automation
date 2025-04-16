# %%
from libs_gspread import get_coupon_gspread_data
from libs_slack import send_chat_slack
from libs_x import post_x


def main(request):
    try:
        request_json = request.get_json(silent=True)
        df = get_coupon_gspread_data()
        print(request_json.get("row_number"))
        post_x(df.at[int(request_json.get("row_number")) - 1, "content"])
        return "200"
    except Exception as e:
        send_chat_slack(f"Xへの投稿に失敗しました。{e}")
        return "500"

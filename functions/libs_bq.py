# %%
from google.cloud import bigquery


def get_product_data() -> dict:
    client = bigquery.Client()
    query = """
        SELECT * FROM `smarthome-428311.sns_automation.view_berry_kagu`
    """
    result = client.query(query).result()
    rows = list(result)
    if not rows:
        raise ValueError("該当商品が見つかりません")
    return dict(rows[0])

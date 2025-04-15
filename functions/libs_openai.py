# %%
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(".env")
openai_api_key = os.getenv("OPENAI_API_KEY")


def generate_post_text(product: dict):
    product_name = product["item_name"]
    # descs = "\n".join(
    #     f"- {product.get(f'item_description{i+1}', '')}"
    #     for i in range(3)
    #     if product.get(f"item_description{i+1}")
    # )
    descs = product["item_description"]
    reviews = "\n".join(
        f"- {product.get(f'point{i+1}', '')}"
        for i in range(1, 4)
        if product.get(f"point{i+1}")
    )
    article_url = product.get("url", "").strip()

    prompt = f"""
あなたはSNSマーケターです。
以下の商品情報をもとに、SNS（X）向けの投稿文を1つ作ってください。
口調はカジュアルで若者向け。テンプレのように"人間が書いた感"がある自然な文章にしてください。
ハッシュタグは3〜5個付けてください。

▼テンプレ例：
---
テンプレ1：
「{{商品名}}」って知ってる？
{{特徴}}で、{{使った人の感想}}もあってちょっと気になってる。
#〇〇 #〇〇

テンプレ2：
まじで盲点だったやつ。
{{商品名}}は{{特徴}}なんだけど、使ってみたら{{レビュー内容}}って感想。
#〇〇 #〇〇
---

▼商品情報：
商品名: {product_name}
特徴:
{descs}
レビュー:{reviews if reviews else ""}
"""

    messages = [
        {
            "role": "system",
            "content": "あなたはSNS投稿を専門にしているマーケターです。",
        },
        {"role": "user", "content": prompt},
    ]

    client = OpenAI(
        api_key=openai_api_key,
    )
    try:
        res = client.chat.completions.create(
            messages=messages, model="gpt-4o-mini", temperature=0.9, max_tokens=300
        )
        text = res.choices[0].message.content.strip()

        # 投稿文の末尾に自メディアリンクを追加（自然な一言つける）
        if article_url:
            text += f"\n\n詳しくはこちら 👉 {article_url}"
        return text
    except Exception as e:
        raise ConnectionError(f"エラーが発生しました: {e}")

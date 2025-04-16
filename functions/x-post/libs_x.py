import os

from dotenv import load_dotenv

load_dotenv(".env")

import tweepy


def post_x(text: str):
    # Twitter API認証情報
    api_key = os.environ.get("X_API_KEY")
    api_secret = os.environ.get("X_API_SECRET")
    access_token = os.environ.get("X_ACCESS_TOKEN")
    access_token_secret = os.environ.get("X_ACCESS_SECRET")

    # 認証
    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )

    try:
        client.create_tweet(text=text)
        return "投稿成功", 200
    except Exception as e:
        return f"エラー発生: {str(e)}", 500

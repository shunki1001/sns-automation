import json
import os

import requests


def send_chat_slack(text: str):
    requests.post(
        os.environ["SLACKE_WEBHOOK"],
        data=json.dumps(
            {
                # メッセージ
                "text": f"<@U06DMN3AMV1>\n{text}",
            }
        ),
    )

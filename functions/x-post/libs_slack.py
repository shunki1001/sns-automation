import json
import os

import requests


def send_chat_slack(text: str):
    requests.post(
        "https://hooks.slack.com/services/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",
        data=json.dumps(
            {
                # メッセージ
                "text": f"<@U06DMN3AMV1>\n{text}",
            }
        ),
    )

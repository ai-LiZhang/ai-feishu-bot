import os
import requests
import datetime

WEBHOOK = os.getenv("https://open.feishu.cn/open-apis/bot/v2/hook/893db3b5-3857-4b75-826a-9fa8ea4f986b")

print("Script started")

today = datetime.date.today()

report = f"""
AI产业投资情报日报

日期：{today}

AI系统测试成功
"""

data = {
    "msg_type": "text",
    "content": {
        "text": report
    }
}

requests.post(WEBHOOK, json=data)

print("Message sent")

import os
import requests
import datetime

print("Script started")

WEBHOOK = os.getenv("https://open.feishu.cn/open-apis/bot/v2/hook/893db3b5-3857-4b75-826a-9fa8ea4f986b")

today = datetime.date.today()

message = f"""
AI系统测试成功

日期：{today}

如果你看到这段文字，
说明 GitHub Actions 已经在运行新的代码。
"""

data = {
    "msg_type": "text",
    "content": {
        "text": message
    }
}

requests.post(WEBHOOK, json=data)

print("Message sent")

import requests
import datetime

WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/893db3b5-3857-4b75-826a-9fa8ea4f986b"

def generate_report():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    return f"AI产业日报 {today}"

def send_to_feishu(text):
    data = {
        "msg_type": "text",
        "content": {
            "text": text
        }
    }
    requests.post(WEBHOOK, json=data)

if __name__ == "__main__":
    send_to_feishu(generate_report())

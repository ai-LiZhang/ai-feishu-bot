import os
import requests

WEBHOOK = os.getenv("https://open.feishu.cn/open-apis/bot/v2/hook/893db3b5-3857-4b75-826a-9fa8ea4f986b")

data = {
    "msg_type": "text",
    "content": {
        "text": "AI系统测试成功"
    }
}

requests.post(WEBHOOK, json=data)

print("test sent")


if __name__ == "__main__":

    main()

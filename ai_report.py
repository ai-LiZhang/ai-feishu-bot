import os
import requests
import datetime

WEBHOOK = os.getenv("https://open.feishu.cn/open-apis/bot/v2/hook/893db3b5-3857-4b75-826a-9fa8ea4f986b")

def main():

    today = datetime.date.today()

    report = f"""
AI产业投资情报日报

日期：{today}

一、AI产业核心事件
- OpenAI 发布新一代 AI Agent 系统
- NVIDIA 推出新一代 AI 推理芯片
- Microsoft 加大 AI 基础设施投资

二、AI技术趋势
AI Agent 与多模态模型持续发展

三、AI投资机会
- AI算力
- AI Agent
- AI机器人
"""

    data = {
        "msg_type": "text",
        "content": {
            "text": report
        }
    }

    print("Sending report...")

    requests.post(WEBHOOK, json=data)

    print("Report sent")


if __name__ == "__main__":
    main()

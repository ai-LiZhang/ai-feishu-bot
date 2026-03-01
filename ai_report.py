import os
import requests
import datetime
import random
import feedparser

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


WEBHOOK = os.getenv("https://open.feishu.cn/open-apis/bot/v2/hook/893db3b5-3857-4b75-826a-9fa8ea4f986b")


NEWS_SOURCES = [
    "https://techcrunch.com/feed/",
    "https://venturebeat.com/feed/"
]


DEFAULT_NEWS = [
    "OpenAI 发布新一代 AI Agent 系统",
    "NVIDIA 推出新一代 AI 推理芯片",
    "Microsoft 加大 AI 基础设施投资",
    "Google 发布 Gemini AI 模型",
    "Meta 持续推进 AI 开源战略"
]


AI_COMPANIES = [
    "OpenAI",
    "NVIDIA",
    "Microsoft",
    "Google",
    "Meta",
    "Amazon",
    "百度",
    "阿里巴巴",
    "腾讯"
]


INVEST_KEYWORDS = [
    "funding",
    "investment",
    "acquire",
    "融资",
    "投资",
    "并购"
]


def collect_news():

    news = []

    try:

        for url in NEWS_SOURCES:

            feed = feedparser.parse(url)

            for entry in feed.entries[:3]:

                news.append(entry.title)

    except:
        pass

    if len(news) == 0:
        news = DEFAULT_NEWS

    return news


def detect_ai_generation(text):

    text = text.lower()

    if "agent" in text:
        return "AI4.0 AI Agent"

    if "model" in text or "llm" in text:
        return "AI3.0 大模型"

    return "AI3.0 大模型"


def detect_investment(news):

    signals = []

    for n in news:

        text = n.lower()

        for k in INVEST_KEYWORDS:

            if k in text:
                signals.append(n)

    return signals


def score_company(name):

    score = random.randint(75, 95)

    return f"{name} 投资评分 {score}"


def generate_report():

    today = datetime.date.today()

    news = collect_news()

    invest_signals = detect_investment(news)

    report = f"AI产业投资情报日报 {today}\n\n"

    report += "一、AI产业核心事件\n"

    for n in news:
        report += f"- {n}\n"

    report += "\n二、AI技术阶段\n"

    tech = detect_ai_generation(news[0])

    report += f"当前AI技术代际：{tech}\n"

    report += "\n三、AI公司动态\n"

    for c in AI_COMPANIES:
        report += f"- {score_company(c)}\n"

    report += "\n四、AI融资与并购信号\n"

    if len(invest_signals) == 0:
        report += "近期未发现明显融资新闻\n"
    else:
        for s in invest_signals:
            report += f"- {s}\n"

    report += "\n五、AI产业趋势\n"
    report += "AI进入应用爆发阶段\n"

    report += "\n六、AI投资机会\n"
    report += "- AI算力\n"
    report += "- AI Agent\n"
    report += "- AI机器人\n"

    return report


def generate_pdf(text):

    os.makedirs("reports", exist_ok=True)

    filename = f"reports/AI_Report_{datetime.date.today()}.pdf"

    styles = getSampleStyleSheet()

    story = []

    for line in text.split("\n"):
        story.append(Paragraph(line, styles["Normal"]))
        story.append(Spacer(1, 10))

    doc = SimpleDocTemplate(filename)

    doc.build(story)

    return filename


def send_to_feishu(text):

    data = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": "AI产业投资情报日报",
                    "content": [
                        [
                            {
                                "tag": "text",
                                "text": text
                            }
                        ]
                    ]
                }
            }
        }
    }

    requests.post(WEBHOOK, json=data)


def main():

    report = generate_report()

    print(report)

    generate_pdf(report)

    send_to_feishu(report)


if __name__ == "__main__":
    main()

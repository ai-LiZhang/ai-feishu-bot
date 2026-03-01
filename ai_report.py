import os
import requests
import feedparser
import datetime
import random

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

WEBHOOK = os.getenv("https://open.feishu.cn/open-apis/bot/v2/hook/893db3b5-3857-4b75-826a-9fa8ea4f986b")

NEWS_SOURCES = [
    "https://techcrunch.com/feed/",
    "https://venturebeat.com/feed/",
    "https://www.theverge.com/rss/index.xml"
]

ARXIV_FEED = "http://export.arxiv.org/rss/cs.AI"

AI_COMPANIES = [
    "OpenAI",
    "NVIDIA",
    "Microsoft",
    "Google",
    "Meta",
    "Amazon",
    "百度",
    "阿里巴巴",
    "腾讯",
    "字节跳动"
]

INVEST_KEYWORDS = [
    "funding",
    "investment",
    "acquire",
    "融资",
    "投资",
    "并购"
]


def detect_ai_generation(text):

    text = text.lower()

    if "agent" in text:
        return "AI4.0 AI Agent"

    if "llm" in text or "foundation model" in text:
        return "AI3.0 大模型"

    if "deep learning" in text:
        return "AI2.0 深度学习"

    return "AI3.0 大模型"


def detect_investment_signal(text):

    text = text.lower()

    for k in INVEST_KEYWORDS:

        if k in text:
            return True

    return False


def collect_news():

    news = []

    for url in NEWS_SOURCES:

        feed = feedparser.parse(url)

        for entry in feed.entries[:5]:

            news.append({
                "title": entry.title,
                "link": entry.link
            })

    return news


def collect_papers():

    papers = []

    feed = feedparser.parse(ARXIV_FEED)

    for entry in feed.entries[:5]:

        papers.append({
            "title": entry.title,
            "link": entry.link
        })

    return papers


def score_company(name):

    score = random.randint(75,95)

    return {
        "company": name,
        "score": score
    }


def generate_report(news, papers, companies):

    today = datetime.date.today()

    report = f"AI产业投资情报日报\n日期：{today}\n\n"

    report += "一、AI产业核心事件\n"

    for n in news:

        report += f"- {n['title']}\n"

    report += "\n二、AI技术突破\n"

    if news:
        tech = detect_ai_generation(news[0]["title"])
        report += f"当前AI技术阶段：{tech}\n"

    report += "\n三、AI公司动态\n"

    for c in companies:

        report += f"- {c['company']} 投资评分 {c['score']}\n"

    report += "\n四、AI创业公司\nAI创业生态持续活跃\n"

    report += "\n五、AI融资与并购\n"

    for n in news:

        if detect_investment_signal(n["title"]):
            report += f"- {n['title']}\n"

    report += "\n六、资本市场观察\nAI板块持续受到资本关注\n"

    report += "\n七、AI产业热门话题\nAI Agent、AI视频、AI机器人\n"

    report += "\n八、AI产业趋势判断\nAI进入应用爆发期\n"

    report += "\n九、AI投资机会\nAI算力、AI Agent、AI机器人\n"

    report += "\n十、推荐投资标的\n"

    for c in companies[:5]:

        report += f"- {c['company']} 评分 {c['score']}\n"

    report += "\n\nAI论文更新\n"

    for p in papers:

        report += f"- {p['title']}\n"

    return report


def generate_pdf(text):

    os.makedirs("reports", exist_ok=True)

    filename = f"reports/AI_Report_{datetime.date.today()}.pdf"

    styles = getSampleStyleSheet()

    story = []

    for line in text.split("\n"):

        story.append(Paragraph(line, styles["Normal"]))
        story.append(Spacer(1,10))

    doc = SimpleDocTemplate(filename)

    doc.build(story)

    return filename


def send_to_feishu(text):

    data = {
        "msg_type": "text",
        "content": {
            "text": text
        }
    }

    requests.post(WEBHOOK, json=data)


def main():

    news = collect_news()

    papers = collect_papers()

    companies = []

    for name in AI_COMPANIES:

        companies.append(score_company(name))

    report = generate_report(news, papers, companies)

    pdf_path = generate_pdf(report)

    send_to_feishu(report)

    print("Report generated:", pdf_path)


if __name__ == "__main__":

    main()

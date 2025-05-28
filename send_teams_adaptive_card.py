import requests
import json
import os
from datetime import datetime
from bs4 import BeautifulSoup

def fetch_article_summaries():
    articles = []

    # Automation World
    aw_url = "https://www.automationworld.com/"
    aw_response = requests.get(aw_url)
    aw_soup = BeautifulSoup(aw_response.content, 'html.parser')
    aw_article = aw_soup.find('div', class_='views-row')
    aw_title = aw_article.find('h2').text.strip()
    aw_summary = aw_article.find('div', class_='field-item').text.strip()
    articles.append({"title": aw_title, "summary": aw_summary})

    # TelcoTitans (AI & Automation)
    tt_url = "https://www.telcotitans.com/network-and-digital/ai-and-automation"
    tt_response = requests.get(tt_url)
    tt_soup = BeautifulSoup(tt_response.content, 'html.parser')
    tt_article = tt_soup.find('div', class_='article')
    tt_title = tt_article.find('h2').text.strip()
    tt_summary = tt_article.find('p').text.strip()
    articles.append({"title": tt_title, "summary": tt_summary})

    # FlowForma News
    ff_url = "https://www.flowforma.com/news"
    ff_response = requests.get(ff_url)
    ff_soup = BeautifulSoup(ff_response.content, 'html.parser')
    ff_article = ff_soup.find('div', class_='news-item')
    ff_title = ff_article.find('h3').text.strip()
    ff_summary = ff_article.find('p').text.strip()
    articles.append({"title": ff_title, "summary": ff_summary})

    return articles

def send_teams_adaptive_card(webhook_url, articles):
    card_body = [
        {
            "type": "TextBlock",
            "size": "Medium",
            "weight": "Bolder",
            "text": "🚀 Weekly News Update"
        },
        {
            "type": "TextBlock",
            "text": "Here are the top 3 articles from Automation World, TelcoTitans, and FlowForma:",
            "wrap": True
        }
    ]

    for article in articles:
        card_body.append({
            "type": "TextBlock",
            "size": "Medium",
            "weight": "Bolder",
            "text": article["title"]
        })
        card_body.append({
            "type": "TextBlock",
            "text": article["summary"],
            "wrap": True
        })

    card_body.append({
        "type": "TextBlock",
        "spacing": "None",
        "size": "Small",
        "isSubtle": True,
        "text": f"Sent on {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC"
    })

    adaptive_card = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "contentUrl": None,
                "content": {
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "type": "AdaptiveCard",
                    "version": "1.2",
                    "body": card_body
                }
            }
        ]
    }

    response = requests.post(
        webhook_url,
        headers={"Content-Type": "application/json"},
        data=json.dumps(adaptive_card)
    )

    if response.status_code == 200:
        print("✅ Message sent successfully.")
    else:
        print(f"❌ Failed to send message. Status code: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    webhook_url = os.getenv("TEAMS_WEBHOOK_URL")
    if not webhook_url:
        raise ValueError("Missing TEAMS_WEBHOOK_URL environment variable")

    articles = fetch_article_summaries()
    send_teams_adaptive_card(webhook_url, articles)

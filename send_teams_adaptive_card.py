import requests
import json
import os
from datetime import datetime

def send_teams_adaptive_card(webhook_url, title, text):
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
                    "body": [
                        {
                            "type": "TextBlock",
                            "size": "Medium",
                            "weight": "Bolder",
                            "text": title
                        },
                        {
                            "type": "TextBlock",
                            "text": text,
                            "wrap": True
                        },
                        {
                            "type": "TextBlock",
                            "spacing": "None",
                            "size": "Small",
                            "isSubtle": True,
                            "text": f"Sent on {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC"
                        }
                    ]
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

    send_teams_adaptive_card(
        webhook_url,
        title="🚀 Daily GitHub Repo Update",
        text="This is a daily update from the GitHub repository."
    )

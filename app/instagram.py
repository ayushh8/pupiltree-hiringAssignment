import requests
from config import INSTAGRAM_API_TOKEN, FACEBOOK_PAGE_ID

def send_instagram_message(user_id, message):
    """Send a message to a user on Instagram."""
    url = f"https://graph.facebook.com/v19.0/{FACEBOOK_PAGE_ID}/messages"
    headers = {
        "Authorization": f"Bearer {INSTAGRAM_API_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {
        "recipient": {"id": user_id},
        "message": {"text": message},
        "messaging_type": "RESPONSE",
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json() 
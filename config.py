import os
from dotenv import load_dotenv

load_dotenv()

INSTAGRAM_API_TOKEN = os.getenv("INSTAGRAM_API_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
FACEBOOK_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")
WEBHOOK_VERIFY_TOKEN = os.getenv("WEBHOOK_VERIFY_TOKEN")
APP_SECRET = os.getenv("APP_SECRET")
DATABASE_FILE = "data/bookings.json" 
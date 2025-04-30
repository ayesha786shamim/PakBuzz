import os
import requests
import feedparser
from twilio.rest import Client
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()
print("To WhatsApp number loaded from .env:", os.getenv("TO_PHONE_NUMBER"))
print(os.getenv("TO_PHONE_NUMBER"))

# === Credentials from .env ===
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")  
TO_PHONE_NUMBER = os.getenv("TO_PHONE_NUMBER")      


def get_news():
    url = "https://www.geo.tv/rss/1/1"
    print(f"Fetching news from: {url}")
    feed = feedparser.parse(url)

    if not feed.entries:
        return "No news found from Geo News."
# === Get Latest Pakistan News ===
# def get_news():
#     url = f"https://newsapi.org/v2/everything?q=pakistan&sortBy=publishedAt&pageSize=4&apiKey={NEWS_API_KEY}"
#     print("Requesting news from:", url)
#     response = requests.get(url)
#     print("Status code:", response.status_code)
#     print("Response text:", response.text)

#     data = response.json()
#     if response.status_code != 200 or not data.get("articles"):
#         return "No news found or error fetching news."

#     headlines = [f"{i+1}. {article['title']}" for i, article in enumerate(data['articles'])]
#     news_message = "*Pakistan News Bot: Latest News*\n\n" + "\n\n".join(headlines)
#     return news_message
    # Get top 4 news articles with links
    
    headlines = [
        f"{i+1}. {entry.title}\n🔗 {entry.link}"
        for i, entry in enumerate(feed.entries[:4])
    ]

    news_message = "*🇵🇰 Geo News Bot: Latest Headlines*\n\n" + "\n\n".join(headlines)
    return news_message

# === Send News via WhatsApp ===
def send_whatsapp(message):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=message,
        from_=TWILIO_PHONE_NUMBER,
        to=TO_PHONE_NUMBER
    )
    print(f"Message sent! SID: {message.sid}")

# === Main Logic ===
if __name__ == "__main__":
    print("Fetching latest news...")
    news = get_news()  # Get the latest news from Pakistan
    print("Sending news to WhatsApp...")
    send_whatsapp(news)  # Send the news to WhatsApp
    print("News successfully sent to WhatsApp!")

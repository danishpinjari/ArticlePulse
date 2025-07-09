from fastapi import FastAPI, Request, Query
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typing import List, Dict, Optional
from dotenv import load_dotenv
import logging
import os
import requests

# ----------------- Load Environment Variables ----------------- #
load_dotenv()

# ----------------- Configuration ----------------- #
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://newsapi.org/v2/"
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# ----------------- FastAPI App Setup ----------------- #
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
analyzer = SentimentIntensityAnalyzer()

# ----------------- News Fetching Function ----------------- #
def get_news(topic: Optional[str] = None , category: Optional[str] = None) -> List[Dict]:
    params = {
        'apiKey': NEWS_API_KEY,
        'language': 'en',
    }

    try:
        if topic:
            endpoint = "everything"
            params.update({'q': topic, 'sortBy': 'relevancy'})
        else:
            endpoint = "top-headlines"
            params.update({
                'country': 'us',
                'category': category if category else 'general'
            })

        response = requests.get(f"{BASE_URL}{endpoint}", params=params, timeout=10)
        response.raise_for_status()
        return response.json().get('articles', [])
    except requests.exceptions.RequestException as e:
        logger.error(f"News API request failed: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error fetching news: {str(e)}")
        return []

def clean_articles(articles: List[Dict]) -> List[Dict]:
    cleaned_articles = []
    for article in articles:
        try:
            if not article.get('title') or '[Removed]' in article.get('title', ''):
                continue
            if not article.get('description') or '[Removed]' in article.get('description', ''):
                continue

            # Set default values
            article.setdefault('urlToImage', '')
            article.setdefault('publishedAt', '')
            article.setdefault('author', 'Unknown')

            # Sentiment analysis
            article['title_sentiment'] = analyzer.polarity_scores(article['title'])
            article['description_sentiment'] = analyzer.polarity_scores(article['description'])

            cleaned_articles.append(article)
        except Exception as e:
            logger.error(f"Error cleaning article: {str(e)}")
            continue

    return cleaned_articles


# ----------------- Home Endpoint ----------------- #
@app.get("/")
async def home(request: Request, topic: Optional[str] = Query(None), category: Optional[str] = Query(None)):
    articles = get_news(topic, category)
    cleaned_articles = clean_articles(articles)

    return templates.TemplateResponse("article.html", {
        "request": request,
        "articles": cleaned_articles,
        "topic": topic,
        "category": category,
    })

# ----------------- Server Entry Point ----------------- #
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

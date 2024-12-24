from fastapi import FastAPI, Request, Query
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import requests

# Initialize the FastAPI app
app = FastAPI()

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Serve static files (CSS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# News API Base URL and Key (replace with your API key)
BASE_URL = "https://newsapi.org/v2/"
NEWS_API_KEY = "2fc2a2999ef544eba64f07e060f086b4"  # Replace with your NewsAPI key

# Function to fetch articles from the News API
def get_news(topic=None, category=None):
    if topic:
        # Fetch news articles based on the topic
        response = requests.get(f"{BASE_URL}everything", params={
            'q': topic,
            'apiKey': NEWS_API_KEY,
            'language': 'en',
            'sortBy': 'relevancy'
        })
    elif category:
        # Fetch top headlines based on the selected category
        response = requests.get(f"{BASE_URL}top-headlines", params={
            'apiKey': NEWS_API_KEY,
            'country': 'us',  # You can change the country if needed
            'category': category,
            'language': 'en'
        })
    else:
        # Fetch general top headlines if no topic or category is provided
        response = requests.get(f"{BASE_URL}top-headlines", params={
            'apiKey': NEWS_API_KEY,
            'country': 'us',  # You can change the country if needed
            'category': 'general'
        })

    articles = response.json().get('articles', [])
    return articles

# Data cleaning function
def clean_articles(articles):
    cleaned_articles = []
    
    for article in articles:
        # Skip articles with removed content or None values
        if not article.get('title') or '[Removed]' in str(article.get('title')) or not article.get('description') or '[Removed]' in str(article.get('description')):
            continue  # Skip this article if title or description contains [Removed]
        
        # Further cleaning to remove any unwanted or irrelevant content like '[Removed]' in the URL, etc.
        if article.get('url') and '[Removed]' in article.get('url'):
            continue  # Skip if URL contains '[Removed]'

        # Append cleaned article
        cleaned_articles.append(article)

    return cleaned_articles

@app.get("/")
async def home(request: Request, topic: str = Query(None), category: str = Query(None)):
    # Fetch news articles based on the topic or category, or general news if none are provided
    articles = get_news(topic, category)
    
    # Clean the articles
    cleaned_articles = clean_articles(articles)
    
    # Return the rendered HTML template with cleaned articles
    return templates.TemplateResponse("article.html", {
        "request": request,
        "articles": cleaned_articles,
        "topic": topic,
        "category": category
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

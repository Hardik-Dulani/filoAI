import requests
from dotenv import load_dotenv
import os
load_dotenv()

os.getenv("GEMINI_API_KEY")

def search_google_custom_api(query, api_key, cse_id):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": api_key,
        "cx": cse_id
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    results = []
    if "items" in data:
        for item in data["items"]:
            results.append({
                "title": item.get("title"),
                "url": item.get("link"),
                "snippet": item.get("snippet")
            })
    
    return results[:20]


import requests
from dotenv import load_dotenv
import os
import streamlit as st
load_dotenv()



def search_google_custom_api(query, api_key, cse_id):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": api_key,
        "cx": cse_id
    }

    response = requests.get(url, params=params)
    data = response.json()
    if not data:
        print('No data captured')
    print(data)
    results = []
    if "items" in data:
        for item in data["items"]:
            results.append({
                "title": item.get("title"),
                "url": item.get("link"),
                "snippet": item.get("snippet")
            })
    print(results)
    return results[:5]
gs_api = os.getenv("gs_api_key")
cse_id = os.getenv("cse_id")
query = st.text_input('')
x = search_google_custom_api(query,gs_api,cse_id)
st.write(x)

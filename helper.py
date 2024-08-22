from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests
import json
import os
import streamlit as st
from PIL import Image
from io import BytesIO
import newspaper
from langchain.text_splitter import TokenTextSplitter 
import prompts




### IMAGE GENERATION

def generate_img(prompt):

    prompt = prompt.replace(" ", "%20")
    image_url = f"https://image.pollinations.ai/prompt/{prompt}"
    
    # Fetch the image from the URL
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))

    # Display the image in Streamlit
    return img
    


def search_google_web_automation(query):
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    
    # Initialize the WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    # Apply stealth settings to minimize detection
    stealth(
        driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    # Define the number of pages to scrape
    n_pages = 2
    results = []
    counter = 0

    try:
        for page in range(1, n_pages + 1):
            url = f"https://www.google.com/search?q={query}&start={(page - 1) * 10}"

            driver.get(url)
            soup = BeautifulSoup(driver.page_source, "html.parser")

            search_results = soup.find_all("div", class_="yuRUbf")

            for result in search_results:
                counter += 1
                title = result.a.h3.text if result.a.h3 else 'No title'
                link = result.a.get("href")
                rank = counter
                results.append({
                    "title": title,
                    "url": link,
                    "domain": urlparse(link).netloc,
                    "rank": rank,
                })
                
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
        
    return results[:3]



def split_text_into_chunks(text, max_tokens):
    text_splitter = TokenTextSplitter(chunk_size=max_tokens, chunk_overlap=0)
    chunks = text_splitter.split_text(text)
    return chunks


def get_article_from_url(url):
    try:
        # Scrape the web page for content using newspaper
        article = newspaper.Article(url)
        # Download the article's content with a timeout of 10 seconds
        article.download()
        # Check if the download was successful before parsing the article
        if article.download_state == 2:
            article.parse()
            # Get the main text content of the article
            article_text = article.text
            return article_text
        else:
            print("Error: Unable to download article from URL:", url)
            return None
    except Exception as e:
        print("An error occurred while processing the URL:", url)
        print(str(e))
        return None


def get_summary_prompt(blog_url):
    # https://learnwithhasan.com/chatgpt-earthquake/
    blog_article = get_article_from_url(blog_url)
    prompt = prompts.summary_prompt + blog_article
    return prompt

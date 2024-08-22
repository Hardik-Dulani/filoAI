from urllib.parse import urlparse
import requests

from PIL import Image
from io import BytesIO
import newspaper




### IMAGE GENERATION

def generate_img(prompt):

    prompt = prompt.replace(" ", "%20")
    image_url = f"https://image.pollinations.ai/prompt/{prompt}"
    
    # Fetch the image from the URL
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))

    # Display the image in Streamlit
    return img
    

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

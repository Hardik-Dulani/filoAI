from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import json

def search_google_web_automation(query):
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument('--ignore-certificate-errors')

    # Exclude automation flags to avoid detection
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    # Enable accepting insecure certificates directly using options
    chrome_options.set_capability("acceptInsecureCerts", True)

    # Initialize the WebDriver with options
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

    for page in range(1, n_pages + 1):
        
        url = f"https://www.google.com/search?q={query}&start={(page - 1) * 10}"
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        search_results = soup.find_all("div", class_="yuRUbf")

        for result in search_results:
            try:
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
                print(f"An error occurred on page {page}: {e}")
                continue  # Move to the next page if an error occurs

    driver.quit()
    return results[:3]

# Example usage
# search_results = search_google_web_automation('Something')
# print(json.dumps(search_results, indent=2))

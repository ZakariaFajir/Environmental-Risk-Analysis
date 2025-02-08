import requests
from bs4 import BeautifulSoup, NavigableString
import xml.etree.ElementTree as ET
import os
from urllib.parse import urlparse, urljoin
import string
from collections import defaultdict

def get_domain_name(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    return domain.replace('www.', '')

import requests
from bs4 import BeautifulSoup, NavigableString
import string
import re

def is_meaningful(text):
    """Filters out unimportant text like menus, copyright, and short phrases."""
    cleaned_text = text.translate(str.maketrans('', '', string.punctuation)).lower()
    words = cleaned_text.split()
    
    # Remove too short text (single words or gibberish)
    if len(words) < 3:
        return False

    # Ignore common website navigation words
    ignored_words = ["privacy policy", "terms", "cookie policy", "about", "contact", "subscribe", "follow us", "related topics"]
    if any(phrase in cleaned_text for phrase in ignored_words):
        return False
    
    return True
  
def extract_image_from_url(soup):
    """Extracts the first relevant image from an article page."""
    img_tag = soup.find("meta", property="og:image")  # Get OpenGraph image if available
    if img_tag and img_tag.get("content"):
        return img_tag["content"]

    img_tag = soup.find("img")  # Fallback to first <img> tag
    if img_tag and img_tag.get("src"):
        return img_tag["src"]

    return None  # No image found

def get_environmental_news(topic):
    """Fetches relevant news articles and extracts meaningful content and images."""
    urls = get_news_urls(topic)
    articles = []

    for url in urls:
        print(f"Scraping article: {url}")
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        article_text = extract_text_from_url(url)
        image_url = extract_image_from_url(soup)

        if article_text and len(article_text) > 100:
            title = article_text.split("\n")[0].replace("Title: ", "")
            summary = " ".join(article_text.split("\n")[1:5])  # Limit summary to 5 lines

            articles.append({
                "title": title,
                "summary": summary,
                "link": url,
                "image": image_url if image_url else None  # Store image URL if available
            })

    return articles

  
def extract_text_from_url(url):
    """Scrapes meaningful text while avoiding error pages and missing content."""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Skipping {url} - HTTP Error {response.status_code}")
        return None  # Skip bad pages

    soup = BeautifulSoup(response.text, 'html.parser')

    # Detect error messages in the page
    error_keywords = ["404 not found", "access denied", "error message", "page not available"]
    page_text = soup.get_text().lower()
    
    if any(error in page_text for error in error_keywords):
        print(f"Skipping {url} - Detected an error page")
        return None

    extracted_text = []
    title = soup.title.string.strip() if soup.title else "No title found"
    extracted_text.append(f"Title: {title}\n")

    # ✅ FIX: Ensure `main_content` is not None
    main_content = soup.find('article') or soup.body
    if main_content is None:
        print(f"Skipping {url} - No valid content found")
        return None

    for element in main_content.find_all(['h1', 'h2', 'h3', 'p']):
        text = element.get_text(strip=True)
        if is_meaningful(text):
            extracted_text.append(text)

    return "\n".join(extracted_text) if extracted_text else None


def get_news_urls(topic):
    """Finds Google News search results for the given topic."""
    search_url = f"https://www.google.com/search?q={topic.replace(' ', '+')}+environmental+risk&tbm=nws"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"Failed to fetch search results: HTTP {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')

        article_links = []
        for result in soup.select("a"):
            link = result.get("href")

            if link and "/url?q=" in link:  # Google redirect format
                clean_link = link.split("/url?q=")[1].split("&")[0]
                
                # Ensure the extracted link is a valid HTTP/HTTPS URL
                if clean_link.startswith("http"):
                    article_links.append(clean_link)

        return article_links[:5]  # Limit to top 5 results

    except requests.RequestException as e:
        print(f"Error fetching Google search results: {e}")
        return []

if __name__ == "__main__":
    topic = "climate change"
    news_data = get_environmental_news(topic)
    for news in news_data:
        print(f"\nTitle: {news['title']}\nSummary: {news['summary']}\nLink: {news['link']}\n")
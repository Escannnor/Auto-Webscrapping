import requests
from bs4 import BeautifulSoup
import re

def safe_request(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def scrape_website(url):
    response = safe_request(url)
    if response:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract main content
        content = extract_main_content(soup)
        
        # Extract links
        links = extract_links(soup)
        
        # Extract images
        images = extract_images(soup)
        
        return {
            "content": content,
            "links": links,
            "images": images
        }
    return None

def extract_main_content(soup):
    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()

    # Get text and format
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    text = re.sub(r'\.(?=\S)', '.\n\n', text)
    
    return text

def extract_links(soup):
    links = []
    for a in soup.find_all('a', href=True):
        links.append({
            "url": a['href'],
            "text": a.get_text(strip=True) or "[No text]"
        })
    return links

def extract_images(soup):
    images = []
    for img in soup.find_all('img', src=True):
        images.append({
            "src": img['src'],
            "alt": img.get('alt', '[No alt text]')
        })
    return images
def scrape_multiple_pages(base_url, num_pages):
    all_text = ""
    for i in range(1, num_pages + 1):
        url = f"{base_url}/page/{i}"
        all_text += scrape_website(url) + "\n\n"
    return all_text

def extract_specific_content(soup, content_type):
    if content_type == "headlines":
        return [h.text for h in soup.find_all(['h1', 'h2', 'h3'])]
    elif content_type == "links":
        return [a['href'] for a in soup.find_all('a', href=True)]
    elif content_type == "images":
        return [img['src'] for img in soup.find_all('img', src=True)]
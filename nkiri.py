import requests
from bs4 import BeautifulSoup

url = 'https://nkiri.com/category/international/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

for data in soup.find_all('article'):
    """title"""
    title = data.find('h2', {'class': 'blog-entry-title entry-title'})
    if title:
        print(title.text.strip())
    
    """image"""
    img = data.find('img')
    if img:
        image = img.get('src')
        print(image)
    
    link = data.find('a', {'class': 'thumbnail-link'})
    if link:
        url_2 = link.get('href')
        print(url_2)
        
        fetch = requests.get(url_2)
        content = BeautifulSoup(fetch.text, 'html.parser')
        
        for item in content.find_all('div', {'class': 'overview'}):
            """Description"""
            desc = item.find('p')
            if desc:
                print(desc.text.strip())
                print('\n')

        # Using Selenium if necessary (e.g., for dynamic content)
        # Ensure you have Edge WebDriver installed and set up correctly
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.edge.options import Options
        
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Edge(options=options)
        driver.get(url_2)

        try:
            # Update the XPath based on the actual structure of the page
            dbtn = driver.find_element(By.XPATH, '/html/body/div[2]/div/main/div/div/div/article/div[1]/div[3]/section[7]/div/div/div/div[2]/div/div/a')
            btn = dbtn.get_attribute('href')  # Usually 'href' for links, not 'src'
            print(btn)
        except Exception as e:
            print("An error occurred:", e)
        finally:
            driver.quit()
    
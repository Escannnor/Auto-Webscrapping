import sqlite3
import requests
from bs4 import BeautifulSoup



base_url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=samsung+s21&_sacat=0&_pgn='
n = range(1, 10)
for num in n:
    url = f'{base_url}{num}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    for data in soup.find_all('li', {'class': 's-item s-item__pl-on-bottom'}):
        product_name = data.find('span', {'role': 'heading'})
        name = product_name.text.strip()
        fig = data.find('span', {'class': 's-item__price'})
        price = fig.text.strip()
        img = data.find('img')
        if img:
            image = img.get('src')
        
        info = data.find('span', {'class': 'SECONDARY_INFO'})
        detail = info.text.strip()
        link = data.find('a')
        if link:
            url =  link.get('href')



connection = sqlite3.connect('product.db')
cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS product (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    price TEXT,
                    url TEXT,
                    image TEXT,
                    detail TEXT)''')





def add_data():
    connection = sqlite3.connect('product.db')
    cursor.executemany("INSERT INTO product (name, price, url, image, detail) VALUES (?, ?, ?, ?, ?)", (name, price, url, image, detail))
    connection.commit()
    return "Product saved"

print(add_data())
from bs4 import BeautifulSoup
import requests, time, random, lxml

url_kara = 'https://kara.com.ng/catalogsearch/result/?q=freezer'
source_kara = requests.get(url_kara).text
soup_kara = BeautifulSoup(source_kara, 'lxml')
for products in soup_kara.find_all('div', class_='product-item-info hover-animation-zoom-item'):
    product_name = products.find('h2', class_='product name product-item-name').text
    price = products.find('span', class_='price').text
    link = products.find('a', class_='product-item-link').get('href')


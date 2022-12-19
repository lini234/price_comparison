from bs4 import BeautifulSoup
import requests, lxml

url = 'https://www.jumia.com.ng/catalog/?q=freezer'
source = requests.get(url).text
soup = BeautifulSoup(source, 'lxml')
res = []
for product in soup.find_all('article', class_='prd _fb col c-prd'):
    product_name = product.h3.text
    price = product.find('div', class_='prc').text
    link = product.find('a', class_='core').get('href')
    product_link = f'https://www.jumia.com.ng{link}'
    res.append((product_name, price, product_link))
    context = {
        'results': res
    }

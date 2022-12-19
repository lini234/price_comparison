from flask import Flask, render_template, request, redirect, url_for, session
from bs4 import BeautifulSoup
import requests, time, random

app = Flask(__name__)
app.secret_key = 'super_secret_key'

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        session['term'] = request.form["srch"]
        term = session['term']
        url = f'https://jumia.com.ng/catalog/?q={term}'
        return redirect(url_for("results", term=term))
    else:
        return render_template('index.html')

@app.route('/results', methods=['GET', 'POST'])
def results():
    page = 1
    term = session.get('term', default=None)
    while page != 10:
        url = f'https://www.jumia.com.ng/catalog/?q={term}r&page={page}#catalog-listing'
        page = page + 1
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
    url_deluxe = f'https://deluxe.com.ng/products?field_product_category=All&text={term}&sort_by=created&page={page}'
    source_deluxe = requests.get(url_deluxe).text
    soup_deluxe = BeautifulSoup(source_deluxe, 'lxml')
    for products in soup_deluxe.find_all('div', class_='product-meta'):
        product_name = products.find('div', class_='field field-title field-type-string field-label-hidden field-item').text
        price = products.find('div', class_='product-price').text
        link = products.find('a', class_='product-title-link').get('href')
        product_link = f'https://deluxe.com.ng{link}'
        res.append((product_name, price, product_link))
    url_kara = f'https://kara.com.ng/catalogsearch/result/index/?p={page}&q={term}'
    source_kara = requests.get(url_kara).text
    soup_kara = BeautifulSoup(source_kara, 'lxml')
    for products in soup_kara.find_all('div', class_='product-item-info hover-animation-zoom-item'):
        product_name = products.find('h2', class_='product name product-item-name').text
        price = products.find('span', class_='price').text
        product_link = products.find('a', class_='product-item-link').get('href')
        res.append((product_name, price, product_link))
    return render_template('results.html', res=res)


# @app.route('/<term>')
# def query(term):
# return render_template('query.html', term=term)


if __name__ == '__main__':
    app.run(debug=True)

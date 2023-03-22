import colorama
import requests
from bs4 import BeautifulSoup
import re
import time


def scrape_details(htmlContent):
    product_dict = {}
    product_index = 1
    products = htmlContent.find_all(
        'div', {'data-component-type': 's-search-result'})

    if not products:
        return None

    colorama.init()
    print(colorama.Fore.YELLOW+"-"*70)
    print(colorama.Fore.YELLOW+"Product Details\n")
    print(colorama.Fore.YELLOW+"-"*70+"\n")

    for product in products:
        name_elem = product.find('span', {'class': 'a-text-normal'})
        name = name_elem.text.strip()
        url = 'https://www.amazon.in' + name_elem.parent['href']
        price = product.find('span', {'class': 'a-price-whole'})
        rating_elem = product.find('span', {'class': 'a-icon-alt'})
        review = product.find(
            'span', {'class': 'a-size-base s-underline-text'})

        if review:
            review = review.text.strip()

        else:
            review = 0

        if rating_elem and price and url and name:
            rating = rating_elem.text.strip()[0:3]
            price = price.text.strip()
            product_dict[product_index] = [name, price, rating, review, url]
            print_product(product_index, name, price, rating, url, review)
            product_index += 1
        else:
            continue

    return product_dict


def print_product(index, name, price, rating, url, review):

    print(colorama.Fore.WHITE+f'Product No: {index} \n')
    print(colorama.Fore.WHITE+f'Name: {name} \n')
    print(colorama.Fore.WHITE+f'Price: {price} \n')
    print(colorama.Fore.WHITE+f'Rating: {rating} \n')
    print(colorama.Fore.WHITE+f'No of reviews: {review} \n')
    print(colorama.Fore.WHITE+f'URL: {url}')
    print(colorama.Fore.YELLOW+"-"*70)


def get_asin(responce):
    try:
        asin = re.search(r'\/dp\/(\w+)\/?', responce.url).group(1)
        if asin == '':
            return "Not available"

        return asin

    except Exception:
        return "Not avaiable"


def get_manufacturer_name(soup):
    try:
        manufacturer = soup.find('a', {'id': 'bylineInfo'})

        if manufacturer.text.strip() == '':
            return 'Not avaiable'
    except Exception:
        return 'Not avaiable'

    return manufacturer.text.strip()


HEADERS = ({'user-agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})


def scrape_individuals(individual):
    index = 1

    for product_list in individual.values():

        response = requests.get(str(product_list[-1]), headers=HEADERS)
        print(colorama.Fore.WHITE+f'{response.status_code}')
        print(colorama.Fore.WHITE+f'{len(response.content)}')

        while len(response.content) <= 8000:
            response = requests.get(str(product_list[-1]), headers=HEADERS)
            time.sleep(5)

        soupIndividual = BeautifulSoup(response.content, 'lxml')
        print(f'Loading {index} ...')
        ASIN = get_asin(response)
        Manufacturer = get_manufacturer_name(soupIndividual)
        product_list.append(ASIN)
        product_list.append(Manufacturer)
        individual[index] = product_list
        index += 1

    return individual

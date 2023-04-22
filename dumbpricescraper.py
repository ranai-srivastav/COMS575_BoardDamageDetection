import requests
from bs4 import BeautifulSoup
import pandas as pd

searchterm = 'lm324'


def get_data(searchterm):
    # searchterm.text.replace(' ','+')
    url = f'https://www.ebay.com/sch/i.html?_from=R40&_nkw={searchterm}&_sacat=0&LH_PrefLoc=1&LH_Auction=1&rt=nc&LH_Sold=1&LH_Complete=1'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


def parse(soup):
    productslist = []
    results = soup.find('div', {'class': 'srp-river-results clearfix'}).find_all('div',
                                                                                 {'class': 's-item__info clearfix'})
    for item in results:
        product = {
            'title': item.find('span', {'role': 'heading'}).text,
            'soldprice': float(
                item.find('span', {'class': 's-item__price'}).text.replace('$', '').replace(',', '').strip()),
            'solddate': item.find('div', {'class': 's-item__title--tagblock'}).find('span', {'class': 'POSITIVE'}).text,
        }
        productslist.append(product)
    return productslist


def output(productslist, searchterm):
    productsdf = pd.DataFrame(productslist)
    productsdf.to_csv(searchterm + 'output.csv_reader', index=False)
    print('Saved to CSV')
    return


soup = get_data(searchterm)
productslist = parse(soup)
output(productslist, searchterm)

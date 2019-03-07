import csv
from typing import Dict, List, Any, Union
import requests
from bs4 import BeautifulSoup as bs

headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'}

base_url = 'https://www.avito.ru/rossiya/tovary_dlya_kompyutera/komplektuyuschie?p=1'


def avito_parse(base_url, headers):
    products: List[Dict[str, Union[str, Any]]] = []
    urls = []
    urls.append(base_url)
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'lxml')
        try:
            pagintaion = soup.find_all('a', attrs={'class': 'pagination-page'})
            count = int(pagintaion[-1].text)
            for i in range(count):
                url = f'https://www.avito.ru/rossiya/tovary_dlya_kompyutera/komplektuyuschie?p={i}'
                if url not in urls:
                    urls.append(url)
        except:
            pass
        for url in urls:
            request = session.get(url, headers=headers)
            divs = soup.find_all('div', attrs={
                'data-marker': 'item'})
            for div in divs:
                try:
                    title = div.find('a', attrs={'itemprop': 'url'}).text
                    href = 'https://www.avito.ru/' + div.find('a', attrs={'itemprop': 'url'})['href']
                    cities = div.find('p').text
                    price = div.find('span', attrs={'itemprop': 'price'})['content'] + 'Р'
                    '''str(price).replace('\n',' ')'''
                    products.append({
                        'title': title,
                        'price': price,
                        'href': href,
                        'cities': cities,
                    })
                except:
                    pass
        for product in products:
            i=i+1
            print(str(i),product)

    else:
        print("Error ", request.status_code)
    return products

avito_parse(base_url, headers)

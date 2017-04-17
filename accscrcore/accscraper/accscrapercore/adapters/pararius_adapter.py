from accscraper.accscrapercore.adapters import Adapter
from accscraper.accscrapercore.utils import remove_non_ascii
from bs4 import BeautifulSoup
import requests


class ParariusAdapter(Adapter):
    def __init__(self):
        self.URL = 'https://www.pararius.com/apartments/nederland/page-{page_number}'
        self.client_name = 'pararius'

    def get_page(self, page_number):
        url = self.URL.format(
            page_number=page_number
        )

        response = requests.get(url)

        if 'there-are-no-results' in response.text:
            return ''

        return response.text

    def process_page(self, page):
        new_apartments = []

        if not page:
            return new_apartments

        page = remove_non_ascii(page)
        soup = BeautifulSoup(page)
        # pretty = soup.prettify()
        apartments = soup.find_all('li', class_='property-list-item-container')
        for apartment_html in apartments:
            id = apartment_html.attrs['data-property-id']

            address = " ".join(apartment_html.find('div', class_='details').find('a').text.split())
            price = " ".join(apartment_html.find('div', class_='details').find('p', class_='price').text.split())
            raw_features = apartment_html.find('div', class_='details').find('ul', class_='property-features').find_all('li')
            raw_location = apartment_html.find('div', class_='details').find('ul', class_='breadcrumbs').find_all('li')

            apartment_features = {}
            for f in raw_features:
                attributes = f.attrs
                apartment_features[attributes['class'][0]] = " ".join(f.text.split())

            location = {
                'address': address,
                'postal_code': raw_location[0].text if len(raw_location) > 0 else '',
                'city': raw_location[1].text if len(raw_location) > 1 else '',
                'city_are': raw_location[2].text if len(raw_location) > 2 else ''
            }

            url = apartment_html.find('div', class_='details').find('p', class_='cta').find('a').attrs['href']

            new_aparment = {
                'client': self.client_name,
                'id': id,
                'price': price,
                'features': apartment_features,
                'url': url,
                'location': location
            }

            new_apartments.append(new_aparment)

        return new_apartments

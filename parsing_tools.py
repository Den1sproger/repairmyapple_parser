import requests
import lxml

from fake_useragent import UserAgent
from bs4 import BeautifulSoup


ua = UserAgent(browsers=['chrome'])

headers = {
    'user-agent': f'{ua.random}'
}



class Search:
    """Basic class with basic functions for site scrapping"""

    def create_soup(self, url: str,
                    class_categories: str,
                    class_link: str) -> list[str]:
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        products = soup.find('div', class_=class_categories).find_all('a', class_=class_link)

        return products


    def create_models_dict(self, url: str) -> dict:
        cards = self.create_soup(
            url=url, class_link='product-link 1',
            class_categories='row no-gutter products-list categories-list'
        )

        models = {}
        for model in cards:
            model_name = model.find('div', class_='product-title').text.strip()
            link = 'https://repairmyapple.ru' + model.get('href')
            models[model_name] = link

        return models


    # def choose_model(self, models: dict) -> str:
    #     print('Please, choose model')

    #     count = 0
    #     for model in models:
    #         count += 1
    #         print(f'{count}) {model}')

    #     while True:
    #         choice = input('Your choice: ')
    #         if choice not in models:
    #             print('There is no such option')
    #         else:
    #             break

    #     return models.get(choice)


    # def input_max_price(self) -> int:
    #     while True:
    #         try:
    #             max_price = int(input('Enter the maximum allowable price (in rubles): '))
    #         except ValueError:
    #             print('Incorrected input!')
    #         else:
    #             break
    #     return max_price


    # def input_device_memory(self) -> int:
    #     variants_of_memory = [2 ** i for i in range(1, 16)]
    #     while True:
    #         memory = int(input('Enter the device memory (in gigabytes): '))
    #         if memory not in variants_of_memory:
    #             print('Incorrect input!')
    #         else:
    #             break

    #     return memory


    def get_price(self, product) -> int:
        return int(product.find('span', class_='current-price').next_element.replace(' ', ''))

    def get_title_text(self, product) -> str:
        return product.find('div', class_='product-title').text.strip()

    def get_product_link(self, product) -> str:
        return 'https://repairmyapple.ru' + product.get('href')

    def __del__(self) -> int:
        return 0



class IPhone(Search):
    """Class for searching the iphones"""

    URL = 'https://repairmyapple.ru/buy/buy-iphone'

    def __init__(self):
        # getting iphone models
        self.models = self.create_models_dict(IPhone.URL)

    def _get_memory(self, text: str, info: str) -> int:
        return int(''.join(text.partition(info)[0:1]).split(' ')[-1])

    def get_products(self, url: str,
                    max_price: int,
                    desired_memory: int) -> list[dict]:
        cards = self.create_soup(   # collecting data about all products of selected model
            url=url, class_link='product-link',
            class_categories='row no-gutter products-list',
        )

        products = []
        for product in cards:
            price = self.get_price(product)
            title_text = self.get_title_text(product)
            link = self.get_product_link(product)
            memory = int

            if 'GB' in title_text:
                memory = self._get_memory(text=title_text, info='GB')

            elif 'Gb' in title_text:
                memory = self._get_memory(text=title_text, info='Gb')

            elif 'TB' in title_text:
                memory = self._get_memory(text=title_text, info='TB') * 1024

            elif 'Tb' in title_text:
                memory = self._get_memory(text=title_text, info='Tb') * 1024

            if price <= max_price and memory == desired_memory:
                parameters = {
                    'link': link,
                    'text': title_text,
                    'price': price
                }
                products.append(parameters)

        return products



class MacBook(Search):
    """Class for searching the macbooks"""

    URL = 'https://repairmyapple.ru/buy/buy-macbook'

    def __init__(self):
        # getting macbook models
        self.models = self.create_models_dict(MacBook.URL)

    def _get_memory(self, text: str,
                    info: str,
                    mb_pro: bool = False) -> int:
        if mb_pro:
            return int(text.partition(';')[2].partition(info)[0].strip())
        else:
            return int(text.partition(info)[0].strip().split(' ')[-1])

    def get_products(self, url: str, max_price: int, desired_memory: int) -> list:
        cards = self.create_soup(   # collecting data about all products of selected model
            url=url, class_link='product-link',
            class_categories='row no-gutter products-list',
        )

        products = []
        for product in cards:
            price = self.get_price(product)
            title_text = self.get_title_text(product)
            link = self.get_product_link(product)
            memory = int

            if ';' in title_text:
                if 'ТБ' in title_text:
                    memory = self._get_memory(text=title_text, info='ТБ', mb_pro=True) * 1024
                else:
                    memory = self._get_memory(text=title_text, info='ГБ', mb_pro=True)
            else:
                if 'ТБ' in title_text:
                    memory = self._get_memory(text=title_text, info='ТБ') * 1024
                else:
                    memory = self._get_memory(text=title_text, info='ГБ')

            if price <= max_price and memory == desired_memory:
                parameters = {
                    'link': link,
                    'text': title_text,
                    'price': price
                }
                products.append(parameters)

        return products



class AirPods(Search):
    """Class for searching the airpods"""

    URL = 'https://repairmyapple.ru/buy/buy-apple/airpods-darom'

    def get_products(self) -> list[dict]:
        cards = self.create_soup(
            url=AirPods.URL,
            class_categories='row no-gutter products-list',
            class_link='product-link'
        )
        products = []
        for product in cards:
            title_text = self.get_title_text(product)
            if 'чехол' in title_text:
                break
            else:
                link = self.get_product_link(product)
                price = self.get_price(product)
                parameters = {
                    'link': link,
                    'text': title_text,
                    'price': price
                }
                products.append(parameters)

        return products



class Apple_Watch(Search):
    """Class for searching the apple watch"""

    URL = 'https://repairmyapple.ru/buy/buy-watch'

    def __init__(self):
        # getting apple watch models
        self.models = self.create_models_dict(Apple_Watch.URL)

    def _get_diagonal(self, text: str) -> int:
        return int(text.partition('mm')[0][-2:])

    def _input_des_diag(self) -> int:
        while True:
            try:
                diag = int(input('Enter the diagonal: '))
            except ValueError:
                print('Incorrected input!')
            else:
                break
        return diag

    def get_products(self, url: str,
                    max_price: int,
                    desired_diagonal: int) -> list[dict]:
        cards = self.create_soup(  # collecting data about all products of selected model
            url=url,
            class_categories='row no-gutter products-list',
            class_link='product-link'
        )

        products = []
        if desired_diagonal != -1:
            for product in cards:
                price = self.get_price(product)
                title_text = self.get_title_text(product)
                link = self.get_product_link(product)
                if 'mm' in title_text:
                    diagonal = self._get_diagonal(title_text)
                    if price <= max_price and diagonal == desired_diagonal:
                        parameters = {
                            'link': link,
                            'text': title_text,
                            'price': price
                        }
                        products.append(parameters)
                else:
                    if price <= max_price:
                        parameters = {
                            'link': link,
                            'text': title_text,
                            'price': price
                        }
                        products.append(parameters)

        else:
            for product in cards:
                price = self.get_price(product)
                title_text = self.get_title_text(product)
                link = self.get_product_link(product)
                if price <= max_price:
                    parameters = {
                        'link': link,
                        'text': title_text,
                        'price': price
                    }
                    products.append(parameters)

        return products



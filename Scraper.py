import requests
from requests.exceptions import ConnectionError
import csv
import re
from bs4 import BeautifulSoup


class Scraper:
    name_list = []
    price_list = []
    rating_list = []
    main_list = []
    product_type = ''

    def __init__(self,product_type):
        Scraper.product_type = product_type

#Collects name, price and rating from given url
    @staticmethod
    def scrape_pages(thread_name, address):
        print("Status: ThreadName: ", thread_name, "url: ", address)
        url = address
        try:
            response = requests.get(url)
        except ConnectionError as e:
            print(e)
        text = response.text
        plain_text = re.sub(r'<!--(.*?)-->', '', text)
        soup = BeautifulSoup(plain_text, "html.parser")

        for link in soup.findAll('div', class_="_3wU53n"):
            Scraper.name_list.append((''.join(link.findAll(text=True))))
        for price in soup.findAll('div', class_="_1vC4OE _2rQ-NK"):
            Scraper.price_list.append((''.join(price.findAll(text=True))[1:]))
        for rating in soup.findAll('div', class_="hGSR34 _2beYZw"):
            Scraper.rating_list.append((''.join(rating.findAll(text=True))[0:-1]))

#Collected data is written into an csv file
    @staticmethod
    def write_to_csv():
        Scraper.main_list = list(zip(Scraper.name_list, Scraper.price_list, Scraper.rating_list))
        file_name = Scraper.product_type + '.csv'
        with open(file_name, 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            for item in Scraper.main_list:
                csv_writer.writerow(item)

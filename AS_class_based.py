import os
import requests
from requests import ConnectionError
from bs4 import BeautifulSoup
import csv

# Global Variables
MAIN_URL = "https://books.toscrape.com/"
FIELDNAMES = ['product_page_url', 'universal_product_code', 'title', 'price_including_tax',
              'price_excluding_tax', 'number_available', 'product_description', 'category',
              'review_rating', 'image_url']

# the folders that will contain the extracts
PATHS = ['extracts/img', 'extracts/csv']

# create the folders if they do not exist
for path in PATHS:
    os.makedirs(path, exist_ok=True)


class SoupObject:
    def __init__(self):
        self.url = None
        self.page = None
        self.soup = None

    def url_soup(self, url):
        self.url = url
        self.page = requests.get(self.url)
        self.soup = BeautifulSoup(self.page.content, 'html.parser')
        return self.soup


class CheckUrl:
    def __init__(self, cls):
        self.cls = cls

    def __call__(self, url):
        self.url = url
        try:
            self.page = requests.get(self.url)
            self.page.raise_for_status()
            return self.cls(url)()
        except ConnectionError:
            return 'The ' + self.cls.__name__ + ' URL ' + self.url + ' is unavailable. ' \
                                                                     'Please check the URL and retry.'
        except requests.exceptions.HTTPError:
            return 'The ' + self.cls.__name__ + ' URL ' + self.url + ' is not accessible. ' \
                                                                     'Please check the URL and retry.'


@CheckUrl
class Book:
    def __init__(self, url):
        self.url = url
        self.soup = SoupObject().url_soup(self.url)

    def __call__(self):
        # self.url = url
        # self.soup = SoupObject().url_soup(self.url)
        # product_page_url
        product_page_url = self.url

        # book title
        book_title = self.soup.find("li", class_="active")
        book_title_text = book_title.text

        # product information  - contained in a table
        book_table_class = self.soup.find("table", class_="table")
        book_table_tds = book_table_class.find_all("td")

        # universal_ product_code (upc)
        universal_product_code = book_table_tds[0].text

        # price_excluding_tax
        price_excluding_tax = book_table_tds[2].text

        # price_including_tax
        price_including_tax = book_table_tds[3].text

        # number_available
        nbr_available_text = book_table_tds[5].text
        nbr_available_cleaned = nbr_available_text.replace("In stock (", "").replace("available)", "").strip()
        number_available = nbr_available_cleaned

        # product_description - contained in <p> tag
        all_p_tags = self.soup.find_all("p")
        product_description = all_p_tags[3].text

        # category - inside the breadcrumb
        breadcrumb = self.soup.find("ul", class_="breadcrumb")
        breadcrumb_links = breadcrumb.find_all("a")
        category = breadcrumb_links[2].text

        # review_rating
        string_to_numbers = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
        star_rating_class = self.soup.find("p", class_="star-rating")['class']
        star_rating_text = star_rating_class[1]
        review_rating = string_to_numbers[star_rating_text]

        # image_url - first image in the book_soup
        image_source = self.soup.find("img")['src']
        image_url = image_source.replace("../..", "http://books.toscrape.com")

        # download the image of the book
        image_page = requests.get(image_url)
        image_file_name = universal_product_code + ".jpg"
        with open('extracts/img/' + image_file_name, "wb") as image_file:
            image_file.write(image_page.content)

        # book data
        book_data = [product_page_url, universal_product_code, book_title_text, price_including_tax,
                     price_excluding_tax, number_available, product_description, category,
                     review_rating, image_url]
        return book_data


@CheckUrl
class Category:

    def __init__(self, url):
        self.category_url_list = []
        self.category_title_list = []
        self.url = url
        self.soup = SoupObject().url_soup(self.url)

    def __call__(self):
        category_url_container = self.soup.find("ul", class_="nav-list")
        category_url_links = category_url_container.find_all("a")

        # loop over the category_url_links to extract the urls and titles to be used as filenames
        for link in range(len(category_url_links)):
            category_url_href = category_url_links[link]["href"]
            category_url_cleaned = MAIN_URL + category_url_href
            self.category_url_list.append(category_url_cleaned)

            category_title = category_url_links[link].text.strip().replace(" ", "_")
            self.category_title_list.append(category_title)
        # remove the first items - the headers
        self.category_url_list.pop(0)
        self.category_title_list.pop(0)
        return self.category_url_list, self.category_title_list


@CheckUrl
class CategoryBookList:
    def __init__(self, url):
        self.url = url
        self.book_url_list = []
        self.url_index = "index.html"
        self.soup = SoupObject().url_soup(self.url)

    def __call__(self):
        category_url_root = self.url.replace(self.url_index, "")
        book_urls = self.soup.find_all("h3")

        # loop over the h3 tags to extract the urls
        for i in range(len(book_urls)):
            book_url_href = book_urls[i].find("a")["href"]
            book_url_cleaned = book_url_href.replace("../../..", "http://books.toscrape.com/catalogue")
            self.book_url_list.append(book_url_cleaned)

        # check whether pagination exists, and if so, get the next page url to extract its books
        if self.soup.find("li", class_="next"):
            next_page_link = self.soup.find("li", class_="next")
            next_page_href = next_page_link.find("a")["href"]
            next_page_url = category_url_root + next_page_href
            self.url_index = next_page_href
            CategoryBookList(next_page_url)
        return self.book_url_list


class Scraper:
    def __init__(self):
        self.book_url_list = []
        self.url_index = "index.html"
        self.category_url_list = Category(MAIN_URL)[0]
        self.category_title_list = Category(MAIN_URL)[1]

    def create_csv(self):
        for (idx, category_url) in enumerate(self.category_url_list):
            filename = "P2_3_Category" + str(idx + 1) + "_" + self.category_title_list[idx] + ".csv"
            self.book_url_list = CategoryBookList(category_url)
            with open('extracts/csv/' + filename, 'w', newline='', encoding='utf-8-sig') as csv_file:
                csv_file_writer = csv.writer(csv_file)
                csv_file_writer.writerow(FIELDNAMES)
                for book_url in self.book_url_list:
                    csv_file_writer.writerow(Book(book_url))
            self.book_url_list = []
            self.url_index = "index.html"


scraper = Scraper()
scraper.create_csv()

"""
task2:
Now that you have obtained the information for one book, you can try and get all the necessary
 information for one category.
Pick any book category on Books to Scrape.
==>Write a Python script that visits this category page and extracts the product
page URL for each book in the category.

Then combine this with the work you have completed to extract the product data
for all the books in your category and write the data to a single CSV file.
Note: some category pages have more than 20 books listed, so they are spread
across different pages (‘pagination’). Your application should be able to handle
this scenario automatically!
"""

import requests
from bs4 import BeautifulSoup
import csv
import os

# the folder that will contain the extracts
path = 'extracts/csv'

# create the folder if it does not exist
os.makedirs(path, exist_ok=True)

# category url to scrape : page of Requiem Red book
category_url = "http://books.toscrape.com/catalogue/category/books/young-adult_21/index.html"
category_url_index = "index.html"

# initialize book urls
book_url_list = []

# csv header
fieldnames = ['product_page_url', 'universal_ product_code', 'title', 'price_including_tax',
              'price_excluding_tax', 'number_available', 'product_description', 'category',
              'review_rating', 'image_url']


# Write a Python script that visits this page and extracts
# the book_data
def extract_book_data(book_page_url):
    book_page = requests.get(book_page_url)
    if book_page:

        # BeautifulSoup object
        book_soup = BeautifulSoup(book_page.content, 'html.parser')

        # product_page_url
        product_page_url = book_page_url

        # title
        book_title = book_soup.find("li", class_="active")
        title = book_title.text

        # product information  - contained in a table
        book_table = book_soup.find("table", class_="table")
        book_table_td = book_table.find_all("td")

        # universal_ product_code (upc)
        universal_product_code = book_table_td[0].text

        # price_excluding_tax
        price_excluding_tax = book_table_td[2].text

        # price_including_tax
        price_including_tax = book_table_td[3].text

        # number_available
        number_available = book_table_td[5].text.replace("In stock (", "").replace("available)", "").strip()

        # product_description - contained in <p> tag
        all_p_tags = book_soup.find_all("p")
        product_description = all_p_tags[3].text

        # category - inside the breadcrumb
        breadcrumb = book_soup.find("ul", class_="breadcrumb")
        breadcrumb_links = breadcrumb.find_all("a")
        category = breadcrumb_links[2].text

        # review_rating
        string_to_numbers = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
        star_rating_class = book_soup.find("p", class_="star-rating")['class']
        star_rating_text = star_rating_class[1]
        for (index, string) in enumerate(string_to_numbers):
            if string == star_rating_text:
                review_rating = string_to_numbers[string]

        # image_url - first image in the book_soup
        image_source = book_soup.find("img")['src']
        image_url = image_source.replace("../..", "http://books.toscrape.com")

        # book data
        book_data = [product_page_url, universal_product_code, title, price_including_tax,
                     price_excluding_tax, number_available, product_description, category,
                     review_rating, image_url]
    return book_data


# Python script that visits this category page and extracts the product page URL
# for each book in the category
def extract_book_urls(category_page_url):
    global category_url_index
    category_page = requests.get(category_page_url)
    category_soup = BeautifulSoup(category_page.content, 'html.parser')
    category_url_root = category_page_url.replace(category_url_index, "")
    book_urls = category_soup.find_all("h3")  # all book urls are in h3 tags, and each in class="product_pod"

    # loop over the h3 tags to extract the urls
    for i in range(len(book_urls)):
        book_url_href = book_urls[i].find("a")["href"]
        book_url_cleaned = book_url_href.replace("../../..", "http://books.toscrape.com/catalogue")
        book_url_list.append(book_url_cleaned)

    # check whether pagination exists, and if so, get the next page url to extract its books
    if category_soup.find("li", class_="next"):
        next_page_link = category_soup.find("li", class_="next")
        next_page_href = next_page_link.find("a")["href"]
        next_page_url = category_url_root + next_page_href
        category_url_index = next_page_href
        extract_book_urls(next_page_url)


# Extract all book urls of chosen category.
extract_book_urls(category_url)

# Write the data to a CSV file.
with open('extracts/csv/P2_2_Scrap_SingleCategoryBooks.csv', 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(fieldnames)
    for url in book_url_list:
        csv_writer.writerow(extract_book_data(url))
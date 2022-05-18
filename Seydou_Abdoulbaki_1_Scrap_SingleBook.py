"""
task1:
Write a Python script that extracts the following information:
    product_page_url
    universal_ product_code (upc)
    title
    price_including_tax
    price_excluding_python tax
    number_available
    product_description
    category
    review_rating
    image_url
Then save the data to a csv file.
"""

import requests
from bs4 import BeautifulSoup
import csv
import os

# The folder that will contain the extracts.
path = 'extracts/csv'

# Create the folder if it does not exist.
os.makedirs(path, exist_ok=True)

# url to scrape : page of Requiem Red book
book_page_url = "http://books.toscrape.com/catalogue/the-requiem-red_995/index.html"
book_page = requests.get(book_page_url)

# csv header
fieldnames = ['product_page_url', 'universal_ product_code', 'title', 'price_including_tax',
              'price_excluding_tax', 'number_available', 'product_description', 'category',
              'review_rating', 'image_url']


# Script that visits the book_page_url and extracts the book_data.
if book_page.status_code == 200:

    # BeautifulSoup object
    book_soup = BeautifulSoup(book_page.content, 'html.parser')

    # product_page_url
    # product_page_url = book_page_url

    # book title
    book_title = book_soup.find("li", class_="active")
    book_title_text = book_title.text

    # product information  - contained in a table
    book_table_class = book_soup.find("table", class_="table")
    book_table_tds = book_table_class.find_all("td")

    # universal_ product_code (upc)
    universal_product_code = book_table_tds[0].text

    # price_excluding_tax
    price_excluding_tax = book_table_tds[2].text

    # price_including_tax
    price_including_tax = book_table_tds[3].text

    # number_available
    number_available_text = book_table_tds[5].text
    number_available_cleaned = number_available_text.replace("In stock (", "").replace("available)", "").strip()

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
    for string in string_to_numbers:
        if string == star_rating_text:
            review_rating = string_to_numbers[string]

    # image_url - first image in the book_soup
    image_source = book_soup.find("img")['src']
    image_url = image_source.replace("../..", "http://books.toscrape.com")

    # book data
    book_data = [book_page_url, universal_product_code, book_title_text, price_including_tax,
                 price_excluding_tax, number_available_cleaned, product_description, category,
                 review_rating, image_url]
else:
    print('The book page is unavailable. Please check the URL and retry again.')

# Write the data to a CSV file.
with open('extracts/csv/P2_1_Scrap_SingleBookPage.csv', 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(fieldnames)
    csv_writer.writerow(book_data)

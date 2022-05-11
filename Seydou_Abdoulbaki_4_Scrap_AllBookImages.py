"""
task4:
download and save the image file for each product page that you visit!
"""

import requests
from bs4 import BeautifulSoup
import csv
import os

# the list of folders that will contain the extracts
paths = ['extracts/img', 'extracts/csv/categories']

# create the folders if they do not exist
for path in paths:
    os.makedirs(path, exist_ok=True)

# category_url_variable
category_url_index = "index.html"

# initialize book urls
book_url_list = []

# initialize category urls
category_url_list = []
category_title_list = []

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

        # get the book image_url = first image in the book_soup
        image_source = book_soup.find("img")['src']
        image_url = image_source.replace("../..", "http://books.toscrape.com")

        # download the image of the book
        image_page = requests.get(image_url)
        image_file_name = universal_product_code + ".jpg"
        with open('extracts/img/'+image_file_name, "wb") as image_file:
            image_file.write(image_page.content)

        # get book data
        book_data = [product_page_url, universal_product_code, title, price_including_tax,
                     price_excluding_tax, number_available, product_description, category,
                     review_rating, image_url]
    return book_data


def extract_book_url(category_page_url):
    global category_url_index
    category_page = requests.get(category_page_url)
    soup = BeautifulSoup(category_page.content, 'html.parser')
    category_url_root = category_page_url.replace(category_url_index, "")
    book_urls = soup.find_all("h3")  # all book urls are in h3 tags, and each in class="product_pod"

    # loop over the h3 tags to extract the urls
    for i in range(len(book_urls)):
        book_url_href = book_urls[i].find("a")["href"]
        book_url_cleaned = book_url_href.replace("../../..", "http://books.toscrape.com/catalogue")
        book_url_list.append(book_url_cleaned)

    # check whether pagination exists, and if so, get the next page url to extract its books
    if soup.find("li", class_="next"):
        next_page_link = soup.find("li", class_="next")
        next_page_href = next_page_link.find("a")["href"]
        next_page_url = category_url_root + next_page_href
        category_url_index = next_page_href
        extract_book_url(next_page_url)


# script that extracts all the book categories available
def extract_category_urls():
    main_url = "http://books.toscrape.com/"
    home_page = requests.get(main_url)
    category_soup = BeautifulSoup(home_page.content, 'html.parser')
    category_url_container = category_soup.find("ul", class_="nav-list")
    category_url_links = category_url_container.find_all("a")

    # loop over the category_url_links to extract the urls and titles for filenames
    for index in range(len(category_url_links)):
        category_url_href = category_url_links[index]["href"]
        category_url_cleaned = main_url + category_url_href
        category_url_list.append(category_url_cleaned)

        category_title = category_url_links[index].text.strip()
        category_title_list.append(category_title)
    # remove the first items - the headers
    category_url_list.pop(0)
    category_title_list.pop(0)


# Extract all category urls
extract_category_urls()

print("There are "+str(len(category_url_list))+" categories")

# Extract all books for each category
for (idx, category_url) in enumerate(category_url_list):
    page = requests.get(category_url)

    if page:
        filename = "P2_3_Category" + str(idx + 1) + "_" + category_title_list[idx] + ".csv"
        extract_book_url(category_url)

    # Write the data to a CSV file.
    with open('extracts/csv/categories/' + filename, 'w', newline='', encoding='utf-8') as csv_file:
        csv_file_writer = csv.writer(csv_file)
        csv_file_writer.writerow(fieldnames)
        for book_url in book_url_list:
            csv_file_writer.writerow(extract_book_data(book_url))
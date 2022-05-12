# OpenClassroom - Python Developer Path

**Project 2:** Use Python Basics for Market Analysis

**Student:** Abdoulbaki Seydou

**Date:** 09/05/2022

# Abstract
In this project, as a marketing analyst at Books Online, a major online bookshop for used books,
our team is tasked to develop a monitoring system that extracts pricing information from 
the Book to Scrape's website[http://books.toscrape.com/], a rival online retailer.

Our monitoring system would therefore need to achieve three tasks: automatically access the website, 
extract the data, and then store it in files. This process is known as web scraping.

We use respectively Requests, BeautifulSoup and CSV, three dedicated Python libraries, for achieving the tasks.

- The repository contains four scripts:

   **1 -** Seydou_Abdoulbaki_1_Scrap_SingleBook.py : extracts the data for a single book, and stores it in a csv file.

   **2 -** Seydou_Abdoulbaki_2_Scrap_SingleCategoryBooks.py : extracts the data for all books in a single category, and stores it in a csv file.

   **3 -** Seydou_Abdoulbaki_3_Scrap_AllBooks.py : extracts the data for all books in all categories, and stores the data in separate csv files per category.

   **4 -** Seydou_Abdoulbaki_4_Scrap_AllBookImages.py : extends the previous by downloading and storing the image for each book.

# Requirement

Latest version of Python must be installed.

You can download the latest version for your system from : https://www.python.org/downloads/

# Installation

**1 - Get the code**

  * $ git clone https://github.com/Afudu/P2_OpenClassroom.git

**2 - Move to the folder**

  * Unix/macOS/Windows: cd P2_OpenClassroom

**3 - Create a virtual environment in the folder P2_OpenClassroom.**

  * Unix/macOS: $ python3 -m venv pythonenv
  * Windows: py -m venv pythonenv
  
    * Note: you can create the virtual environment in another folder, then move to that folder to run the command above.
    * Example: in the above command, our virtual environment created is called pythonenv - you can give a different name.

**4 - Activate the virtual environment created**

  * Unix/macOS: $ source pythonenv/bin/activate

  * Windows: pythonenv\Scripts\activate

**5 - Securely upgrade pip**

 * Unix/macOS/Windows: pip install --upgrade pip

**6 - Install all dependencies**

 * Unix/macOS/Windows: pip install -r requirements.txt

# Running the code

To run each of the four scripts, in the terminal (Unix, macOS) or command line (Windows), type python followed by the file name then hit Enter:

  python script_file.py

Example: to run the first script, type the below command and then hit Enter.

  python Seydou_Abdoulbaki_1_Scrap_Book.py

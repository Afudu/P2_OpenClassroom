# Use Python Basics for Market Analysis


**OpenClassrooms - Python Developer Path:** Project 2

**Student:** Abdoul Baki Seydou

**Date:** 09/05/2022

## Table of Contents
1. [Summary](#summary)
2. [Technologies Used](#technologies-used)
3. [Project Tasks](#project-tasks)
4. [Local Development](#local-development)
   - [Prerequisites](#prerequisites)
   - [Setup on macOS/Linux](#setup-on-macoslinux)
   - [Setup on Windows](#setup-on-windows)
   - [Running the Application](#running-the-application)
   - [Linting](#linting)

## Summary
This project involves developing a monitoring system for Books Online, 
a major online retailer specializing in used books. 
As a marketing analyst,  the goal is to extract and monitor pricing information from a competitor's website,
[Book to Scrape](http://books.toscrape.com/).  The system will scrape book data and store it for analysis.

## Technologies Used
- **Programming Language:** Python  
- **Libraries:** Requests, BeautifulSoup and CSV.


## Project Tasks
1. Code extracting data of single book, and store it in a csv file.
2. Code extracting data of all books in a single category, and store it in a csv file.
3. Code extracting data of all books in all categories, and store it in a csv file.
4. Code extending the previous by downloading and storing the image of each book.


## Local Development

### Prerequisites
- PostgreSQL installed.
- Python 3.6 or higher.

### Setup on macOS/Linux

1. **Clone the Repository**
   ```bash
   cd /path/to/put/project/in
   git clone https://github.com/Afudu/P2_OpenClassroom.git

2. **Move to the folder**
   ```bash
   cd P2_OpenClassroom

3. **Set Up Virtual Environment**
   ```bash
   python -m venv venv
   
4. **Activate Environment**
   ```bash
   source venv/bin/activate 

5. **Securely upgrade pip**
   ```bash
   python -m pip install --upgrade pip 

6. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   
7. **To deactivate Environment**
   ```bash
   deactivate

### Setup on Windows

1. Follow the steps above.

2. To activate the environment:
   ```bash
   .\venv\Scripts\Activate

### Running the application

* The repository contains four scripts:

    **1 -** AS_1_Scrap_SingleBook.py : Extracts the data for a single book.

    **2 -** AS_2_Scrap_SingleCategoryBooks.py : Extracts the data for all books in a single category.

    **3 -** AS_3_Scrap_AllBooks.py : Extracts the data for all books across all categories.

    **4 -** AS_4_Scrap_AllBookImages.py : Extends the previous by storing the image for each book.


* To execute a script:
   ```bash
   python script_file_name.py
  
* **Output**: The data extracted by each script is saved in the ```extracts``` folder, 
   which is created upon execution.

### Linting
The codebase is fully linted and free of errors.
- **To Run Linting**
  ```bash
  flake8

"""
1. Make a CSV file named 'companies.csv' with the company names in the same folder as this file
2. Utilize the *requests* library to send HTTP requests to a search engine, *BeautifulSoup* to parse the HTRM content
3. Use the *csv* module to read and write a CSV file with the search contents
"""

# 1. Import modules
import requests
from bs4 import BeautifulSoup
import csv

# 2. Set a user agent to mimic a web browser 
    # (avoid being flagged as a bot and blocked)
url = 'https://www.google.de/search'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
}

# read companies file into python list
with open("companies.csv", "r") as file:
    reader = csv.reader(file)
    companies = list(reader)

# for each company name in list, send request to search engine for website URL 
# and parse HTML content using BeautifulSoup to find the first result (usually website)
with open("results.csv", "w", newline="") as result_file:
    writer = csv.writer(result_file)
    for row in companies:
        company = row[0]
        # params is what goes into the search bar in each request
        params = {"q": f"{company} -site:appexchange.salesforce.com"}
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # check first result
            result = soup.find("div", class_="g")

            # add results to "results.csv"
            if result:
                website_url = result.find("a").get("href")
                print(f"{company}: {website_url}")
                writer.writerow([company, website_url])
            else:
                writer.writerow([company, "No website found"])
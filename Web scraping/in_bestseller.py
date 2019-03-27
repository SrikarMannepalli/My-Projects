import re
import requests
import bs4
import csv
totallist = []
rowlist = ["Name", "URL", "Author", "Price",
           "Number of Ratings", "Average Rating"]
totallist.append(rowlist)
with open("./output/in_book.csv", "w") as file:
    writing = csv.writer(file)
    for row in totallist:
        writing.writerow(row)
file.close

from bs4 import BeautifulSoup
pageids = ["https://www.amazon.in/gp/bestsellers/books/ref=zg_bs_pg_1?ie=UTF8&pg=1", "https://www.amazon.in/gp/bestsellers/books/ref=zg_bs_pg_2?ie=UTF8&pg=2",
           "https://www.amazon.in/gp/bestsellers/books/ref=zg_bs_pg_2?ie=UTF8&pg=3", "https://www.amazon.in/gp/bestsellers/books/ref=zg_bs_pg_2?ie=UTF8&pg=4", "https://www.amazon.in/gp/bestsellers/books/ref=zg_bs_pg_2?ie=UTF8&pg=5"]
k = 0
for k in range(0, 5):
    page = requests.get(pageids[k])
    soup = BeautifulSoup(page.content, "html.parser")
    midpart = soup.findAll(id="zg_centerListWrapper")
    elements = midpart[0].findAll(class_="zg_itemImmersion")
    i = 0
    for num in elements:
        i += 1
    names = []
    prices = []
    authors = []
    ratings = []
    avgrat = []
    url = []

    for j in range(0, i, 1):
        if elements[j].find(class_="p13n-sc-truncate p13n-sc-line-clamp-1") == None:
            names = "not available"
        else:
            names = elements[j].find(
                class_="p13n-sc-truncate p13n-sc-line-clamp-1").get_text().encode("UTF-8").strip()

        if elements[j].find(class_="p13n-sc-price") == None:
            prices = "not available"
        else:
            prices = elements[j].find(
                class_="p13n-sc-price").get_text().encode("UTF-8").strip()
        if elements[j].find(class_="a-size-small") == None:
            authors = "not available"
        else:
            authors = elements[j].find(
                class_="a-size-small").get_text().encode("UTF-8").strip()
        if elements[j].find(class_="a-icon-row a-spacing-none") == None:
            ratings = "not available"
        elif elements[j].find(class_="a-icon-row a-spacing-none").find(class_="a-link-normal") == None:
            ratings = "not available"
        else:
            ratings = elements[j].find(
                class_="a-icon-row a-spacing-none").find(class_="a-link-normal").get("title")
        if elements[j].find(class_="a-size-small a-link-normal") == None:
            avgrat = "not available"
        elif elements[j].find(class_="a-size-small a-link-normal").get_text().encode("UTF-8").strip() == None:
            avgrat = "not available"
        else:
            avgrat = elements[j].find(
                class_="a-size-small a-link-normal").get_text().encode("UTF-8").strip()

        if elements[j].find('a')['href'] == None:
            url = "not available"
        else:
            url = "http://www.amazon.in" + elements[j].find('a')['href']

        rowlist = [names, url, authors, prices, ratings, avgrat]
        totallist.append(rowlist)
        with open("./output/in_book.csv", "w") as file:
            writing = csv.writer(file)
            for row in totallist:
                writing.writerow(row)
        file.close

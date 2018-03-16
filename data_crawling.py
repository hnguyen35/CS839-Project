import csv
import requests
from bs4 import BeautifulSoup

ATTRIBUTES = ['Homepage', 'Revenue', 'Original Language', 'Runtime', 'Budget', 
              'Genres', 'Content Score']

def get_entity(url):
    """For each url, returns an entity with attributes in ATTRIBUTES."""
    source = requests.get(url, allow_redirects = True)
    plain_text = source.text  # call attribute 'text' of object 'source'
    soup = BeautifulSoup(plain_text, 'html.parser')
    entity = {} 
    for att in ATTRIBUTES:
        entity[att] = '-'

    # Extract attribute from fact section.
    facts_section = soup.find("section", class_="facts left_column")
    for line in facts_section.get_text().split('\n'):
        for att in ATTRIBUTES:
            if line.startswith(att):
                value = line.replace(att, '').strip()
                entity[att] = value

    # Extract attribute from genres section.
    genres_section = soup.find("section", class_="genres right_column")
    genres = []
    for line in genres_section.find_all("li"):
        genres.append(line.get_text())

    entity['Genres'] = ",".join(genres)

    # Construct data to be written to CSV.
    row = []
    for att in ATTRIBUTES:
        row.append(entity[att])
    return row

def get_urls():
    """Returns all links to crawl."""
    urls = ['https://www.themoviedb.org/movie/122-the-lord-of-the-rings-the-return-of-the-king']
    """
    START_PAGE = 'https://www.themoviedb.org/movie/top-rated?page=%s'
    for i in range(1, 2):
        page_url = START_PAGE % str(i)
        print ('Craw for movie links on page: ' + page_url)
        source = requests.get(page_url, allow_redirects = True)
        plain_text = source.text  # call attribute 'text' of object 'source'
        soup = BeautifulSoup(plain_text, 'html.parser')
        for a in soup.find_all("a", class_="title result"):
            movie_url = 'https://www.themoviedb.org' + a.get('href')
            urls.append(movie_url)
    """
    return urls

def main():
    """
    This is comment in python 
    for multiple lines
    """
    csvfile = open('movies.csv', 'w')
    writer = csv.writer(csvfile, delimiter='|')
    writer.writerow(ATTRIBUTES)
    for url in get_urls():
        writer.writerow(get_entity(url))

if __name__ == "__main__":
    main()

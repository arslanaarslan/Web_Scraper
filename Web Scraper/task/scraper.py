import string
import re
import os

import requests
from bs4 import BeautifulSoup

def fetch_pages(number_of_pages, type_of_article):
    for page in range(1, number_of_pages + 1):
        try:
            os.mkdir(f"Page_{page}")
            # print(f"Page_{page} folder created")
        except OSError:
            print(f"Creation of the Directory Page_{page} failed")

        url = f"https://www.nature.com/nature/articles?sort=PubDate&year=2020&page={page}"
        response = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            articles = soup.find_all('article')

            news = []

            for article in articles:
                article_type_data = article.find('span', {'class': 'c-meta__type'}).string
                # print(article_type_data)
                if article_type_data == type_of_article:
                    news.append(article)

            news_headers = []
            news_links = []

            for news_item in news:
                news_header = news_item.find('a').string
                # string_1 = news_header.translate(str.maketrans('', '', string.punctuation))
                string_2 = re.sub(r'[^\w\s\’]', '', news_header)
                string_3 = string_2.replace(" ", "_") + ".txt"
                news_headers.append(string_3)

                news_link = news_item.find('a')['href']
                news_links.append("https://www.nature.com" + news_link)

            # print(news_links)
            article_texts = []

            for link in news_links:
                response = requests.get(link, headers={'Accept-Language': 'en-US,en;q=0.5'})

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    article_text = soup.find('p', {'class': 'article__teaser'}).text

                article_texts.append(article_text)

            for i in range(len(news_headers)):
                with open(f"Page_{page}/{news_headers[i]}", "w") as file:
                    file.write(article_texts[i])

        else:
            print(f'The URL returned {response.status_code}')


number_of_pages = int(input())
type_of_article = input()
fetch_pages(number_of_pages, type_of_article)

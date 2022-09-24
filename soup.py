from turtle import title
import requests
from bs4 import BeautifulSoup
import pandas as pd

metro_stations = requests.get('https://en.wikipedia.org/wiki/List_of_Washington_Metro_stations')

metro_stations_content = metro_stations.content


soup = BeautifulSoup(metro_stations_content, "html.parser")

tables = soup.find_all('a')
titles = soup.find_all(attrs="title")
links = []
clean_links = []

for link in tables:
    links.append(link.get_text())

for l in links:
    if l != '':
        clean_links.append(l)









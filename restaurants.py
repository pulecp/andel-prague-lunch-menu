#!/usr/bin/env python
from bs4 import BeautifulSoup
from urllib.request import urlopen

def bernard(day):

    out = {}

    bernard_file = urlopen("https://www.bernardpub.cz/pub/andel")
    bernard_html = bernard_file.read()
    bernard_file.close()

    soup = BeautifulSoup(bernard_html, "lxml")
    for food_list in soup.find_all("div", { "id" : "day-selection-tab-"+day }):
        for food in food_list.find_all("div", { "class" : "single-food" }):
            name = food.strong.contents[0]
            price = food.find_all("span", { "class" : "food-price" })[0].contents[0]
            out[name] = price
            #print("Food: {}, price: {}".format(name,price))

    return out

def run(day):

    restaurants = {}

    restaurants['bernard'] = bernard(day)

    return restaurants


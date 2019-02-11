#!/usr/bin/env python

#
# Many thanks to Pavel Grochal (https://github.com/Darkless012) who provided the parsers
# for Zomato.cz and Menicka.cz !!!
#

import urllib
import os
import json
from bs4 import BeautifulSoup


def zomato(url):
    menu = []

    try:
        zomato_apikey = ENV['ZOMATO_APIKEY']
    except:
        # use export ZOMATO_APIKEY=<zomato_api_key> before you start this application locally
        zomato_apikey = os.environ.get('ZOMATO_APIKEY')

    HEADERS = {
        'user_key': zomato_apikey,
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0'
    }

    zomato_request = urllib.request.Request(url, headers=HEADERS)
    zomato_response = urllib.request.urlopen(zomato_request)
    zomato_data = json.load(zomato_response)
    zomato_response.close()

    try:
        dishes = zomato_data.get('daily_menus', [{}])[0].get('daily_menu', {}).get('dishes', [{}])
        for x in dishes:
            dish = x.get('dish', {})
            menu.append([dish.get('name'), dish.get('price')])
    except:
        pass

    return menu


def menicka(url):
    menu = []

    menicka_request = urllib.request.urlopen(url)
    menicka_response = menicka_request.read()
    menicka_request.close()

    soup = BeautifulSoup(menicka_response, "lxml")

    try:
        menicka = soup.select('.menicka')
        if len(menicka) >= 1:
            first_menu = menicka[0]
            elements = first_menu.find_all("div", class_="nabidka_1 cena".split())

            completion = []

            for element in elements:
                element_classes = element.get('class', [])
                if "nabidka_1" in element_classes:
                    completion.append([element.get_text()])
                if "cena" in element_classes:
                    completion[-1].append(element.get_text())

            for item in completion:
                if len(item) == 0:
                    continue
                if len(item) == 1:
                    menu.append([item[0], ""])
                if len(item) >= 2:
                    menu.append([item[0], item[1]])
    except:
        pass

    return menu


def bernard():
    menu = []

    bernard_file = urllib.request.urlopen("https://www.bernardpub.cz/pub/andel")
    bernard_html = bernard_file.read()
    bernard_file.close()

    soup = BeautifulSoup(bernard_html, "lxml").find('section', {'class': 'daily-menu'})
    for food_list in soup.find_all("ul", {"class": "food-list"}):
        for food in food_list.find_all("div", {"class": "single-food"}):
            name = food.strong.contents[0]
            price = food.find_all("span", {"class": "food-price"})[0].contents[0]
            menu.append([name, price])

    return menu


def run():
    with open('restaurants.json') as f:
        restaurants = json.load(f)

    for restaurant in restaurants:
        if restaurant['type'] == 'bernard':
            try:
                restaurant['menu'] = bernard()
            except:
                pass
        elif restaurant['type'] == 'zomato':
            try:
                restaurant['menu'] = zomato(
                "https://developers.zomato.com/api/v2.1/dailymenu?res_id=" + restaurant['zomatoId'])
            except:
                pass
        elif restaurant['type'] == 'menicka':
            try:
                restaurant['menu'] = menicka(restaurant['menickaLink'])
            except:
                pass
    return restaurants

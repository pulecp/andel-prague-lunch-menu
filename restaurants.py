#!/usr/bin/env python

#
# Many thanks to Pavel Grochal (https://github.com/Darkless012) who provided the parsers
# for Zomato.cz and Menicka.cz !!!
#

import urllib
import os
import json
from bs4 import BeautifulSoup
import datetime


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

    # try:
    menicka = soup.select('.menicka')

    try:
        if len(menicka) >= 1:
            first_menu = menicka[0]
            today_menu = first_menu.find_all("li")

            completion = []
            for item in today_menu:
                food = item.find('div', {'class': 'polozka'})
                if food is not None:
                    completion.append([food.get_text()])

                    price = item.find('div', {'class': 'cena'})
                    if price is not None:
                        completion[-1].append(price.get_text())

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

    body = BeautifulSoup(bernard_html, "lxml")
    datetab = body.find(text=datetime.datetime.today().__format__('%-d. %-m.'))

    if datetab:
        menu_id = datetab.parent.parent['data-tab-target']
    else:
        menu_id = body.find(attrs={"class": "day-selection-tab"})['id']

    for food in body.find(id=menu_id).find_all("div", {"class": "single-food"}):
        name = food.strong.contents[0]
        price = food.find_all("span", {"class": "food-price"})[0].contents[0]
        menu.append([name, price])

    return menu


def run(filename):
    with open('pages/'+filename) as f:
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
        elif restaurant['type'] == 'link':
            pass
    return restaurants

#!/usr/bin/env python

#
# Many thanks to Pavel Grochal (https://github.com/Darkless012) who provided the parsers
# for Zomato.cz and Menicka.cz !!!
#

import urllib
import os
import json
import pprint
import datetime
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

    zomato_request = urllib.request.Request(url, headers = HEADERS)
    zomato_response = urllib.request.urlopen(zomato_request)
    zomato_data = json.load(zomato_response)
    zomato_response.close()

    try:
        dishes = zomato_data.get('daily_menus',[{}])[0].get('daily_menu',{}).get('dishes',[{}])
        for x in dishes:
            dish = x.get('dish',{})
            menu.append([dish.get('name'),dish.get('price')])
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
        if len(menicka) >=1:
            first_menu = menicka[0]
            elements = first_menu.find_all("div", class_="nabidka_1 cena".split())

            completion = []

            for element in elements:
                element_classes = element.get('class',[])
                if "nabidka_1" in element_classes:
                    completion.append([element.get_text()])
                if "cena" in element_classes:
                    completion[-1].append(element.get_text())

            for item in completion:
                if len(item) == 0:
                    continue
                if len(item) == 1:
                    menu.append([item[0],""])
                if len(item) >= 2:
                    menu.append([item[0],item[1]])
    except:
        pass

    return menu

def bernard(day):

    menu = []

    bernard_file = urllib.request.urlopen("https://www.bernardpub.cz/pub/andel")
    bernard_html = bernard_file.read()
    bernard_file.close()

    soup = BeautifulSoup(bernard_html, "lxml")
    for food_list in soup.find_all("div", { "id" : "day-selection-tab-"+day }):
        for food in food_list.find_all("div", { "class" : "single-food" }):
            name = food.strong.contents[0]
            price = food.find_all("span", { "class" : "food-price" })[0].contents[0]
            menu.append([name,price])
            #print("Food: {}, price: {}".format(name,price))

    return menu

def run():

    restaurants = {
        'Bernard pub':       { 'link': 'https://www.bernardpub.cz/pub/andel' },
        'Mr. Bao':           { 'link': 'https://www.mrbao.cz/'},
        'U Kristiána':       { 'link': 'http://www.ukristiana.cz/#restaurace-ukristiana'},
        'Formanka':          { 'link': 'http://www.smichovskaformanka.cz/'},
        'Tradice':           { 'link': 'http://www.tradiceandel.cz/'},
        'Na Ztracené':       { 'link': 'http://www.naztracene.cz/'},
        'Klub Santoška':     { 'link': 'http://www.klubsantoska.cz/'},
        'Akcent':            { 'link': 'http://www.akcentrestaurant.cz/'},
        'Bife':              { 'link': 'http://www.biferestaurant.cz/'},
        'Radegastovna Perón':{ 'link': 'http://peronsmichov.cz/'},
        'Plachta':           { 'link': 'http://www.plachta.cz/'},
        'Lokal Blok':        { 'link': 'http://www.lokalblok.cz/'},
    }

    restaurants['Bernard pub']['menu'] = bernard(str(datetime.datetime.today().isoweekday()))
    restaurants['Mr. Bao']['menu'] = zomato("https://developers.zomato.com/api/v2.1/dailymenu?res_id=18337487")
    restaurants['U Kristiána']['menu'] = menicka("https://www.menicka.cz/2323-restaurace-u-kristiana.html")
    restaurants['Formanka']['menu'] = zomato("https://developers.zomato.com/api/v2.1/dailymenu?res_id=16506447")
    restaurants['Tradice']['menu'] = menicka("https://www.menicka.cz/2305-puor-tradice.html")
    restaurants['Na Ztracené']['menu'] = menicka("https://www.menicka.cz/2324-na-ztracene.html")
    restaurants['Klub Santoška']['menu'] = menicka("https://www.menicka.cz/2238-klub-santoska.html")
    restaurants['Akcent']['menu'] = zomato("https://developers.zomato.com/api/v2.1/dailymenu?res_id=16510836")
    restaurants['Bife']['menu'] = menicka("https://www.menicka.cz/4591-bife-restaurant.html")
    restaurants['Radegastovna Perón']['menu'] = menicka("https://www.menicka.cz/456-radegastovna-per%F3n.html")
    restaurants['Plachta']['menu'] = menicka("https://www.menicka.cz/2249-restaurace-plachta.html")
    restaurants['Lokal Blok']['menu'] = menicka("https://www.menicka.cz/2207-lokal-blok.html")

    #pprint.pprint(restaurants)

    return restaurants


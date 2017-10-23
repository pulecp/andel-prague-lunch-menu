#!/usr/bin/env python

# bernard
from bs4 import BeautifulSoup

# mr.bao
import pdftotext
import re

# general
import urllib
import os
import json

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

#  DEPRACATED, mr_bao was replaced by zomato
#
#
#
# def mr_bao(day):
# 
#     menu = []
# 
#     mrbao_file = urllib.request.urlopen("http://www.mrbao.cz/menu/")
#     mrbao_html = mrbao_file.read()
#     mrbao_file.close()
# 
#     # soup = BeautifulSoup(mrbao_html, "lxml")
#     # print(soup.find_all("a", { "class" : "btn btn-large" }))
#     
#     #with open("mr_bao.pdf", "rb") as f:
#     #    pdf = pdftotext.PDF(f)
#     
#     # bug: you would need to parse the proper URL from (http://www.mrbao.cz/menu/) because it's changing every week
#     url = urllib.request.urlopen('http://www.mrbao.cz/wp-content/uploads/2017/07/%E6%96%B0%E7%89%88-Poledn%C3%AD-menu_CZ_R.pdf')
#     pdf = pdftotext.PDF(url)
# 
#     for line in pdf[0].split('\n'):
#         stripped_line = re.sub(' +',' ',line.strip())
# 
#         # try to find price
#         pattern = re.compile(".*(1[0-9][0-9]K.).*")
#         match = pattern.search(stripped_line)
#         if match:
#             price = match.group(1)
#             # remove a price from stripped line
#             stripped_line = re.sub(".1[0-9][0-9]K.","",stripped_line)
#         else:
#             price = ""
# 
#         # a detail to a meal can be on a newline starting with '('
#         if stripped_line.startswith('('):
#             menu[-1][0] = menu[-1][0] + stripped_line
#         else:
#             menu.append([stripped_line, price])
# 
#     # # uncomment for debugging
#     # counter=0
#     # for line in menu:
#     #     print(str(counter) + line[0] + line[1])
#     #     counter += 1
# 
#     if day == "1":
#         return [menu[2],menu[3],menu[4],menu[5]]
#     if day == "2":
#         return [menu[7],menu[8],menu[9],menu[10]]
#     if day == "3":
#         return [menu[12],menu[13],menu[14],menu[15]]
#     if day == "4":
#         return [menu[17],menu[18],menu[19],menu[20]]
#     if day == "5":
#         return [menu[22],menu[23],menu[24],menu[25]]

def zomato(url):

    menu = []

    try:
        zomato_apikey = ENV['ZOMATO_APIKEY']
    except:
        # use export ZOMATO_APIKEY=<zomato_api_key> before you start this application locally
        zomato_apikey = os.environ.get('ZOMATO_APIKEY')

    HEADERS = {
        'user_key': zomato_apikey,
        'Accept': 'application/json'
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


def run(day):

    restaurants = {}

    restaurants['bernard pub'] = bernard(day)
    restaurants['mr. bao'] = zomato("https://developers.zomato.com/api/v2.1/dailymenu?res_id=18337487")

    return restaurants


import urllib
import json
from bs4 import BeautifulSoup
import re


def menicka(url):
    menu = []

    menicka_request = urllib.request.urlopen(url)
    menicka_response = menicka_request.read()
    menicka_request.close()

    soup = BeautifulSoup(menicka_response, "html.parser")

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
                if len(item) >= 2:
                    food = re.sub(r'(^\d+\. )|(\d{3}g)', '', item[0])
                    price = re.findall(r'\d+', item[1])
                    if int(price[0]) > 100:
                        menu.append([food, item[1]])
    except:
        pass

    return menu


def prague_catering(url):
    menu = []

    page = urllib.request.urlopen(url)
    html = page.read()
    page.close()

    body = BeautifulSoup(html, "html.parser")
    table = body.find(attrs={"class": "dennimenu"})

    for row in table.find_all("tr"):
        info = row.find_all("td")
        if info[0].text == 'Salátový bar 100g':
            break

        if (info[1].text.strip() is not ''):
            name = info[0].text
            price = info[1].text
            menu.append([name, price])

    return menu


def process(filename):
    with open('pages/' + filename + '.json') as f:
        restaurants = json.load(f)

    for restaurant in restaurants:
        if restaurant['type'] == 'menicka':
            try:
                restaurant['menu'] = menicka(restaurant['menicka_link'])
            except:
                pass
        elif restaurant['type'] == 'link':
            pass
    return restaurants

from bs4 import BeautifulSoup
from requests import get
import PySimpleGUI as sg


def convertingPriceIntoNumeric(price_):
    digits = price_.split(" ")
    price_ = ''
    for d in digits:
        if d != "zł":
            price_ += d
    price_ = price_.replace(',', '.')
    return float(price_)


def concatURL(url_, city_, house_, flat_, price_limit_, min_area_, max_area_):
    url_list_ = [url_]
    if flat_ and house_:
        url_list_ = [url_, url_]
        url_list_[0] += "mieszkania/"
        url_list_[1] += "domy/"
    elif house_:
        url_list_[0] += "domy/"
    elif flat_:
        url_list_[0] += "mieszkania/"
    for iterator in range(0, len(url_list_)):
        url_list_[iterator] += city_
        url_list_[iterator] += "?search%5Bfilter_float_price%3Ato%5D="
        url_list_[iterator] += str(price_limit_)
        url_list_[iterator] += "&search%5Bfilter_float_m%3Afrom%5D="
        url_list_[iterator] += str(min_area_)
        url_list_[iterator] += "&search%5Bfilter_float_m%3Ato%5D="
        url_list_[iterator] += str(max_area_)
    return url_list_


url = 'https://www.olx.pl/nieruchomosci/'


sg.theme("SandyBeach")

layout = [
    [sg.Text('Hello, this app will help you to find the cheapest real estate offers on OLX')],
    [sg.Text('Enter information about offers you are interested in')],
    [sg.Text('City', size=(15, 1)), sg.InputText()],
    [sg.Text('Price limit', size=(15, 1)), sg.InputText()],
    [sg.Text('Minimum Area', size=(15, 1)), sg.InputText()],
    [sg.Text('Maximum Area', size=(15, 1)), sg.InputText()],
    [sg.Text('How many offers?', size=(15, 1)), sg.InputText()],
    [sg.Checkbox("I'm looking for a house", default=True)],
    [sg.Checkbox("I'm looking for a flat", default=True)],
    [sg.Submit(), sg.Cancel()],
    [sg.Output(size=(150, 20))]
]


window = sg.Window('Real estate offers', layout)

while True:
    event, values = window.read()
    if event == 'Close':
        window.close()
        break

    city = values[0]
    price_limit = int(values[1])
    min_area = int(values[2])
    max_area = int(values[3])
    amount = int(values[4])
    house = values[5]
    flat = values[6]

    url_list = concatURL(url, city, house, flat, price_limit, min_area, max_area)

    offers = {}

    for url in url_list:
        page = get(url)
        bs = BeautifulSoup(page.content, features="html.parser")
        for offer in bs.find_all('div', class_='offer-wrapper'):
            price = offer.find('p', class_='price').get_text().strip()
            price = convertingPriceIntoNumeric(price)
            source = offer.find("a")
            source = source["href"]
            # Because of people who advertise house/flat rent in sell category, we need to have min price to avoid
            # rent offers
            if price > 8000:
                offers[price] = source
    sorted_offers = sorted(offers)
    for i in range(0, amount):
        print("Price:", end=" ")
        print(sorted_offers[i], end="  Link: ")
        print(offers.get(sorted_offers[i]))
        print(" ")
    window.refresh()





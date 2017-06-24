#!/usr/bin/env python
from contextlib import closing
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup, SoupStrainer
import pickle
import datetime

address = "url_here"

print "Fetching sauce"
try:
    with closing(Firefox()) as browser:
        browser.get(address)
        WebDriverWait(browser, timeout=10).until(
            lambda x: x.find_element_by_link_text("Daily Deals"))
        page_source = browser.page_source

    print "Making soup"
    soup = BeautifulSoup(page_source, 'lxml')
    deals = []

    print "Straining"
    for url in soup.find_all('div', class_='daily-deal-item group active'):
        pid = url.a.get('href').encode('ascii', 'ignore').decode('ascii').rsplit('/', 1)[-1]
        name = url.find('div', class_='deal-info').h3.text.encode('ascii', 'ignore').decode('ascii')
        link = url.a.get('href').encode('ascii', 'ignore').decode('ascii')
        dp = url.find('div', class_='deal-info').div.p.text.encode('ascii', 'ignore').decode('ascii')
        lp = url.find('div', class_='deal-info').div.div.p.text.encode('ascii', 'ignore').decode('ascii')

        deal = (pid, name, link, dp, lp)
        deals.append(deal)

    print "Pickling"
    try:
        with open(str(datetime.datetime.now()), 'wb') as f:
            pickle.dump(deals, f)
            print "Soup's up"
    except:
        print "Jar broke"

except:
    print "Shop's closed"

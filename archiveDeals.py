#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup, SoupStrainer
import pickle
import datetime

#Note: This now requires the PhantomJS driver

deals = []

def getHTML(url, title):
    browser = webdriver.PhantomJS('phantomjs')
    browser.get(url)
    WebDriverWait(browser, timeout=20).until(
        lambda x: x.find_element_by_link_text(title))
    return browser.page_source

def getDeals(html):
    soup = BeautifulSoup(html, 'lxml')
    deals = []
    for url in soup.find_all('div', class_=r'daily-deal-item group active'):
        try:
            pid = url.a.get('href').encode('ascii', 'ignore').decode('ascii').rsplit('/', 1)[-1]
            name = url.find('div', class_='deal-info').h3.text.encode('ascii', 'ignore').decode('ascii')
            link = url.a.get('href').encode('ascii', 'ignore').decode('ascii')
            dp = url.find('div', class_='deal-info').div.p.text.encode('ascii', 'ignore').decode('ascii')
            try:
                lp = url.find('div', class_='deal-info').div.div.p.text.encode('ascii', 'ignore').decode('ascii')
            except:
                lp = 0

            deal = (pid, name, link, dp, lp)
            deals.append(deal)

        except Exception as e:
            print(e)
    return deals

def moreDeals(html):
    soup = BeautifulSoup(html, 'lxml')

    paginator = soup.find('div', class_='filter-paginator pagination')

    n = None

    for url in paginator.find_all('a'):
        try:
            if url.get('rel') == ['next']:
                n = url.get('href')
        except:
            pass

    return n

def scrapePage(address, title):
    try:
        page_source = getHTML(address, title)

        deals.extend(getDeals(page_source))

        n = moreDeals(page_source)

        if (n != None):
            address = 'https://'+address.split('/')[2]+n
            scrapePage(address, title)
        else:
            pass
    except Exception as e:
        print(e)

if __name__ == '__main__':
    title = ""
    address = ""

    scrapePage(address, title)

    try:
        with open(str(datetime.datetime.now()), 'wb') as f:
            pickle.dump(deals, f)
            print "Got "+str(len(deals))+" pickels!"

    except Exception as e:
        print(e)

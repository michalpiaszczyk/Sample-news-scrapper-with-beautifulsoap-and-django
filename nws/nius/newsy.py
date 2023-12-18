from bs4 import BeautifulSoup
import requests
from datetime import datetime
import configparser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from django.core.mail import send_mail

config = configparser.ConfigParser()
config.read(r'config.ini')
start_date_str = config.get('DEFAULT', 'start_date')
start_date = datetime.strptime(start_date_str, '%Y-%m-%d')

today = datetime.today()


def trzy_doliny():
    url = 'https://trzydoliny.eu'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    divs = soup.find_all('div', class_='r_desc')
    newsy = []
    for div in divs:
        title = div.find('div', class_='prod_name').text.strip()
        try:
            date_str = div.find('div', class_='dodano').text.strip()[
                len('Data dodania: '):]
        except AttributeError:
            date_str = start_date.strftime('%Y-%m-%d')
            pass
        date = datetime.strptime(date_str, '%Y-%m-%d')
        try:
            link = url+'/' + \
                div.find('div', class_='prod_name').find('a')['href']
        except TypeError:
            link = 'brak'
            pass
        try:
            desc = div.find('div', class_='txt')
            tekst = desc.text.strip()
            usun = div.find('span', style='font-size: 18px;').text.strip()
            desc = tekst.replace(usun, '')
        except AttributeError:
            desc = "Brak"
            pass
        if date >= start_date:
            news = {'title': title, 'date': date, 'link': link,
                    'desc': desc, 'source': 'https://trzydoliny.eu'}
            newsy.append(news)
    return newsy


def rzadowe():
    urls = ['https://www.gov.pl/web/cppc/lista-aktualnosci', 'https://www.gov.pl/web/uw-kujawsko-pomorski/wiadomosci2', 'https://www.gov.pl/web/fundusze-regiony/aktualnosci1', 'https://www.gov.pl/web/sport/wiadomosci',
            'https://www.gov.pl/web/premier/wydarzenia', 'https://www.gov.pl/web/infrastruktura/aktualnosci', 'https://www.gov.pl/web/edukacja-i-nauka/wiadomosci', 'https://www.gov.pl/web/sport/dofinansowanie-zadan-z-funduszu-rozwoju-kultury-fizycznej-201948']
    newsy = []
    for url in urls:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        divs = soup.find_all('div', class_='art-prev art-prev--near-menu')

        for div in divs:
            titles_divs = div.find_all('div', class_='title')
            titles_list = [title.get_text() for title in titles_divs]
            dates = soup.find_all('span', {'class': 'date'})
            dates_str_list = [date.get_text().strip() for date in dates]
            dates_list = [datetime.strptime(
                date_str, '%d.%m.%Y') for date_str in dates_str_list]
            links = div.find_all('a')
            links_urls = ['https://www.gov.pl'+link['href'] for link in links]
            desc = []
            for a in links:
                try:
                    intro = a.find('div', {'class': 'intro'}).text.strip()
                except:
                    intro = "Brak opisu"
                desc.append(intro)
            
            temp_news = []
            while len(dates_list)< len(titles_list):
                dates_list.append(datetime.today())
            for i in range(len(titles_list)):
                temp_news.append(
                    {'title': titles_list[i], 'date': dates_list[i], 'link': links_urls[i], 'desc': desc[i], 'source': url})
            temp_news = [x for x in temp_news if x['date'] >= start_date]
            newsy.extend(temp_news)
    return newsy

def mojrerpo():
    newsy = []
    url = 'https://mojregion.eu/rpo/wiadomosci/'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    # ------titles--------#
    titles = [post.h2.a.text for post in soup.find_all("div", class_="post")]
    titles = [title.replace('\n', '').replace('\t', '') for title in titles]
    # ------links--------#
    links = [post.h2.a["href"] for post in soup.find_all("div", class_="post")]
    # ------dates--------#
    dates_str = [post.div.span.text.strip()
                 for post in soup.find_all("div", class_="post")]
    dates_str = [date_str[:10] for date_str in dates_str]
    dates = [datetime.strptime(date_str, '%d.%m.%Y') for date_str in dates_str]
    for i in range(len(titles)):
        newsy.append({'title': titles[i], 'date': dates[i],
                     'link': links[i], 'desc': 'Brak opisu', 'source': url})
    newsy = [x for x in newsy if x['date'] >= start_date]

    return newsy


def mojprow():
    url = 'https://mojregion.eu/prow/aktualnosci/'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    newsy = []

    # ------titles--------#
    titles = [post.h2.a.text for post in soup.find_all("div", class_="post")]
    titles = [title.replace('\n', '').replace('\t', '') for title in titles]

    # ------links--------#
    links = [post.h2.a["href"] for post in soup.find_all("div", class_="post")]

    # ------dates--------#
    dates_str = [post.div.span.text.strip()
                 for post in soup.find_all("div", class_="post")]
    dates = [datetime.strptime(date_str, '%Y-%m-%d %H:%M')
             for date_str in dates_str]

    # ------descr--------#
    descs = [post.p.get_text() for post in soup.find_all("div", class_="post")]
    descs = [desc.replace('\n', '').replace('\t', '') for desc in descs]
    # print(descs[0])

    for i in range(len(titles)):
        newsy.append({'title': titles[i], 'date': dates[i],
                     'link': links[i], 'desc': descs[i], 'source': url})
    newsy = [x for x in newsy if x['date'] >= start_date]
    return newsy


def efr():
    url = 'https://efrwp.pl/'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    newsy = []
    # ------titles--------#
    titles = [link.h2.text.strip()
              for link in soup.find_all("a", class_="postlink_wide")]

    # ------links--------#
    links = [link["href"]
             for link in soup.find_all("a", class_="postlink_wide")]
    # ------dates--------#
    dates_str = [link.span.text.strip()
                 for link in soup.find_all("a", class_="postlink_wide")]
    dates = [datetime.strptime(date_str, '%d/%m/%y') for date_str in dates_str]
    # ------descr--------#
    descs = [link for link in soup.find_all('div', class_="postlink_wide__r")]
    meta_div = soup.find('div', class_='postlink_wide__meta')
    for desc in descs:
        h2 = desc.find('h2')
        if meta_div:
            meta_div.extract()
        if h2:
            h2.extract()
    descs = [desc.get_text() for desc in descs]
    descs = [desc.replace('\n', ' ').replace(
        '\t', '').replace('\xa0', ' ') for desc in descs]
    for i in range(len(titles)):
        newsy.append({'title': titles[i], 'date': dates[i],
                     'link': links[i], 'desc': descs[i], 'source': url})
    newsy = [x for x in newsy if x['date'] >= start_date]
    return newsy


def sow():

    url = 'https://portal-sow.pfron.org.pl/opencms/export/sites/pfron-sow/sow/aktualnosci/'
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    try:
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.presence_of_element_located(
            (By.TAG_NAME, 'ng-binding')))
    except:
        pass

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    newsy = []

    # ------titles--------#
    titles = [h2.text.strip()
              for h2 in soup.find_all("h2", class_="ng-binding")]
    titles = [' '.join(title.split()) for title in titles]

    # ------links--------#
    links = ['https://portal-sow.pfron.org.pl'+link["href"]
             for link in soup.find_all("a", class_="item-wrapper")]
    # # ------dates--------#
    dates_str = [dts.span.text.strip()
                 for dts in soup.find_all("div", class_="col-5 date")]
    dates = [datetime.strptime(date_str, '%Y-%m-%d') for date_str in dates_str]

    # ------descr--------#
    descs = [desc.p.get_text()
             for desc in soup.find_all('div', class_="ng-binding")]
    descs = [' '.join(desc.split()) for desc in descs]
    # ------stwórz słownik--------#
    for i in range(len(titles)):
        newsy.append({'title': titles[i], 'date': dates[i],
                     'link': links[i], 'desc': descs[i], 'source': url})

    newsy = [x for x in newsy if x['date'] >= start_date]
    return newsy

new_start_date = datetime.now().date()
config.set('DEFAULT', 'start_date', new_start_date.strftime('%Y-%m-%d'))

with open(r'config.ini', 'w') as f:
    config.write(f)

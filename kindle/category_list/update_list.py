
import json
import pandas as pd
from numpy import nan
from bs4 import BeautifulSoup
from selenium import webdriver 

kindle_best_sellers = {
    'Australia':'https://www.amazon.com.au/gp/bestsellers/digital-text/2496751051/ref=zg_bs_unv_kinc_2_2496752051_1',
    'Brazil':'https://www.amazon.com.br/gp/bestsellers/digital-text/5475882011/ref=zg_bs_nav_kinc_1_kinc',
    'Canada':'https://www.amazon.ca/Best-Sellers-Kindle-Store-eBooks/zgbs/digital-text/2980423011/ref=zg_bs_nav_kinc_1_kinc',
    'China':'https://www.amazon.cn/Kindle%E7%94%B5%E5%AD%90%E4%B9%A6/b?ie=UTF8&node=116169071&ref_=nav_topnav_giftcert',
    'France':'https://www.amazon.fr/gp/bestsellers/books/ref=zg_bs_nav_0',
    'Germany':'https://www.amazon.de/gp/bestsellers/digital-text/530886031/ref=zg_bs_nav_kinc_1_kinc',
    'India':'https://www.amazon.in/gp/bestsellers/digital-text/1634753031/ref=zg_bs_nav_kinc_1_kinc',
    'Italy':'https://www.amazon.it/gp/bestsellers/digital-text/827182031/ref=zg_bs_nav_kinc_1_kinc',
    'Japan':'https://www.amazon.co.jp/-/en/gp/bestsellers/digital-text/2275256051/ref=zg_bs_nav_kinc_1_kinc',
    'Mexico':'https://www.amazon.com.mx/gp/bestsellers/digital-text/6507977011/ref=zg_bs_nav_kinc_1_kinc',
    'Netherlands':'https://www.amazon.nl/gp/bestsellers/digital-text/4550510031/ref=zg_bs_nav_kinc_1_kinc',
    'Poland':'https://www.amazon.pl/gp/bestsellers/books/ref=zg_bs_nav_0',
    # 'Saudi Arabia':'',
    'Singapore':'https://www.amazon.sg/gp/bestsellers/books/ref=zg_bs_nav_0',
    'Spain':'https://www.amazon.es/gp/bestsellers/digital-text/827231031/ref=zg_bs_nav_kinc_1_kinc',
    'Sweden':'https://www.amazon.se/gp/bestsellers/books/ref=zg_bs_nav_0',
    'Turkey':'https://www.amazon.com.tr/gp/bestsellers/books/ref=zg_bs_nav_0',
    'United Arab Emirates':'https://www.amazon.ae/gp/bestsellers/books/ref=zg_bs_nav_0',
    'United States' : 'https://www.amazon.com/Best-Sellers-Kindle-Store-eBooks/zgbs/digital-text/154606011/ref=zg_bs_nav_kstore_1_kstore',
    'United Kingdom': 'https://www.amazon.co.uk/Best-Sellers-Kindle-Store-eBooks/zgbs/digital-text/341689031/ref=zg_bs_nav_kinc_1_kinc'
}

kindle_categories_us    = {}


class kindle:
    count = 0
    browser = None

    def category(self, country='United States'):
        self.browser = webdriver.Chrome('../../chromedriver.exe') 
        self.browser.get(kindle_best_sellers[country])
        soup = BeautifulSoup(self.browser.page_source, features='lxml')
        ul = soup.find('ul', attrs={'id':'zg_browseRoot'})
        ul = ul.find('ul')
        ul = ul.find('ul')
        our_ul = ul.find('ul')
        li_list = our_ul.find_all('li')
        for li in li_list:
            self.count += 1
            cat = li.get_text()
            link = li.find('a')['href']
            kindle_categories_us[cat] =  self.check_subcategory(cat, link)
            print(self.count, '- "' + cat + '"', ' : ', kindle_categories_us[cat], '\n')
            with open(country + '.json', 'w+') as jasonfile:
                json.dump(kindle_categories_us, jasonfile, indent=4)
        self.browser.close()
        
    def check_subcategory(self, cat, link):
        cat_dict = {}
        self.browser.get(link)
        soup = BeautifulSoup(self.browser.page_source, features='lxml')
        li = soup.find('span', attrs={'class':'zg_selected'}).parent
        ul = li.parent
        try:
            our_ul = ul.find('ul')
            cat_dict['null'] = link 
            li_list = our_ul.find_all('li')
            for li in li_list:
                cat = li.get_text()
                link = li.find('a')['href']
                cat_dict[cat] =  self.check_subcategory(cat, link)
        except: return link
        return cat_dict


def selected_countries():
    countries =  pd.read_excel('countries.xlsx', 'countries')
    datas = countries['countries']
    country_list = []
    for i in datas.index:
            if datas[i] is not nan:    
                country_list.append(datas[i])
    return country_list

if __name__ == '__main__':
    kind = kindle()
    selectedcountries = selected_countries()
    for country in kindle_best_sellers:
        if country in selectedcountries:
            # kind.category(country)
            print(country)


    
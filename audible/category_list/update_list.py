
import json
import pandas as pd
from numpy import nan
from bs4 import BeautifulSoup
from selenium import webdriver 

audible_best_sellers    = {
    'Australia': 'https://www.amazon.com.au/gp/bestsellers/audible/ref=zg_bs_nav_0',
    'Brazil': '',
    'Canada': 'https://www.amazon.ca/Best-Sellers-Audible-Audiobooks/zgbs/audible/ref=zg_bs_nav_0',
    'China': '',
    'France': 'https://www.amazon.fr/gp/bestsellers/audible/ref=zg_bs_nav_0',
    'Germany': 'https://www.amazon.de/gp/bestsellers/audible/ref=zg_bs_nav_0',
    'India': 'https://www.amazon.in/gp/bestsellers/audible/ref=zg_bs_nav_0',
    'Italy': 'https://www.amazon.it/gp/bestsellers/audible/ref=zg_bs_nav_0',
    'Japan': 'https://www.amazon.co.jp/-/en/gp/bestsellers/audible/ref=zg_bs_nav_0',
    # 'Mexico': '',
    # 'Netherlands': '',
    # 'Poland': '',
    # 'Saudi Arabia': '',
    # 'Singapore': '',
    # 'Spain': '',
    # 'Sweden': '',
    # 'Turkey': '',
    # 'United Arab Emirates': '',
    'United Kingdom': 'https://www.amazon.co.uk/Best-Sellers-Audible-Audiobooks/zgbs/audible/ref=zg_bs_nav_0',
    'United States' : 'https://www.amazon.com/Best-Sellers-Audible-Audiobooks/zgbs/audible/?_encoding=UTF8&ref_=sv_adbl_subnav_ref1_2'
}

audible_categories_us   = {}


class audible:
    count = 0
    browser = None

    def category(self, country='United States'):
        self.browser = webdriver.Chrome('../../chromedriver.exe') 
        self.browser.get(audible_best_sellers['United States'])
        soup = BeautifulSoup(self.browser.page_source, features='lxml')
        ul = soup.find('ul', attrs={'id':'zg_browseRoot'})
        ul = ul.find('ul')
        our_ul = ul.find('ul')
        li_list = our_ul.find_all('li')
        for li in li_list:
            self.count += 1
            cat = li.get_text()
            link = li.find('a')['href']
            audible_categories_us[cat] =  self.check_subcategory(cat, link)
            print(self.count, '- "' + cat + '"', ' : ', audible_categories_us[cat], '\n')
            with open(country + '.json', 'w+') as jasonfile:
                json.dump(audible_categories_us, jasonfile, indent=4)
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
    audi = audible()
    selectedcountries = selected_countries()
    for country in audible_best_sellers:
        if country in selectedcountries:
            # audi.category(country)
            print(country)

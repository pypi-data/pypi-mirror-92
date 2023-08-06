import os
import sqlite3
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm


class VOAScraper:
    '''
    Dependencies: Chromedriver
    Args:
        driver_path: str, Path to chromedriver executable file
        out_path:  [Optional] str, Path to output directory. If unspecified, current directory will be used
        chromedriver_proxy: dict, A dictionary containing proxy information for the webdriver
    '''
    def __init__(self, driver_path, out_path=None, chromedriver_proxy=None):

        assert os.path.isfile(driver_path), "Invalid Chromedriver path received"

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('log-level=3')
        if chromedriver_proxy is not None:
            webdriver.DesiredCapabilities.CHROME['proxy'] = chromedriver_proxy
        self.driver = webdriver.Chrome(driver_path, options=chrome_options)

        print("Output file: ",
              os.path.join(out_path, 'VOAArticles.db') if out_path else 'VOAArticles.db')

        self.conn = sqlite3.connect(
            os.path.join(out_path, 'VOAArticles.db') if out_path else 'VOAArticles.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS ARTICLES (ID INTEGER PRIMARY KEY AUTOINCREMENT,"
                       "HEADING TEXT,"
                       "CONTENT TEXT,"
                       "AUTHOR TEXT,"
                       "LINK TEXT)")

    def _get_links(self, num_scrolls):
        all_links = []
        self.driver.get('https://www.voanews.com/usa')
        for _ in range(num_scrolls):
            self.driver.execute_script('''document.querySelector("a[rel='next']").click()''')
            time.sleep(2)

        bs4_page = BeautifulSoup(self.driver.page_source, 'lxml')
        anchor_tags = bs4_page.findAll('a', {'class': 'teaser__title-link'})
        for a in anchor_tags:
            all_links.append("https://www.voanews.com" + a['href'])

        return all_links

    def _get_article_content(self, links):
        for link in tqdm(links):
            try:
                p_list = []
                page = BeautifulSoup(requests.get(link).content, 'lxml')
                title = page.find('h1', {'class': 'page-header__title'}).find('span').text
                author = page.find('div', {'class': 'page-header__meta-item'}).findAll('span')[-1].text
                p_tags = page.find('div', {'class': 'article__body'}).find('div').findAll('p')

                for p in p_tags:
                    p_list.append(p.text)
                full_content = '\n'.join(p_list)
                self.cursor.execute("INSERT INTO ARTICLES VALUES (?,?,?,?,?)", (None, title, full_content, author, link))
                self.conn.commit()
            except Exception:
                continue

    def scrape(self, num_scrolls=1):
        '''
        Scraper function for Voice of America News articles
        num_scrolls: int, Number of times to fetch more entries. Default is 1
        '''
        assert (type(num_scrolls) == int and num_scrolls >= 0), "Number of scrolls cannot be negative"
        all_links = self._get_links(num_scrolls)
        self._get_article_content(all_links)
        self.conn.close()
        self.driver.close()

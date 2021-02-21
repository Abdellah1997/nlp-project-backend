from bs4 import BeautifulSoup
import requests
from urllib.request import Request, urlopen 
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd

class WebScrapper():

    def __init__(self, url, no_of_pagedowns=10):
        self.url = url
        self.no_of_pagedowns = no_of_pagedowns
    
    def get_html(self, url):
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(url,headers=hdr)
        page = urlopen(req)
        soup = BeautifulSoup(page, features="html.parser")
        return soup
        
    def get_article(self, soup):
        article =  soup.findAll("div", {"class": "article-content"})[0]
        return article.get_text()
    
    def get_title(self, soup):
        title =  soup.findAll("h1", {"class": "post-title"})[0]
        return title.get_text()
    
    def get_articles_url(self):
        driver = webdriver.Chrome()
        driver.get(self.url)

        time.sleep(1)
        elem = driver.find_element_by_tag_name("body")

        while self.no_of_pagedowns:
            elem.send_keys(Keys.PAGE_DOWN)
            time.sleep(2)
            self.no_of_pagedowns-=1

        soup = BeautifulSoup(driver.page_source,'html.parser')
        div_articles = soup.findAll("div", {"class": "posts-categoy"})[0]
        articles =[]
        for link in div_articles.find_all('a'):
            articles.append(link.get('href'))
        return articles
    
    def save_articles(self, file_name):
        articles_url = self.get_articles_url()
        articles = []
        titles = []
        for url in articles_url:
            soup = self.get_html(url)
            articles.append(self.get_article(soup))
            titles.append(self.get_title(soup))
        
        df = pd.DataFrame({'title': titles, 'article': articles})
        df.to_csv(file_name)

if __name__ == "__main__":
    webScrapper = WebScrapper('https://www.hespress.com/politique',20)
    webScrapper.save_articles('hespress_politique.csv')
 



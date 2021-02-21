from bs4 import BeautifulSoup
import requests
from urllib.request import Request, urlopen 
import time
import pandas as pd

class HespressScrapper():

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
        divs = soup.findAll("div", {"class": "article-content"})
        if len(divs) > 0 :
            article =  divs[0]
            return article.get_text()
        return ""
    
    def get_title(self, soup):
        h1s = soup.findAll("h1", {"class": "post-title"})
        if len(h1s) > 0:
            title =  h1s[0]
            return title.get_text()
        return ""
    
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
        news =[]
        for url in articles_url:
            soup = self.get_html(url)
            article = self.get_article(soup)
            title = self.get_title(soup)
            if article != "" and title != "":
                articles.append(article)
                titles.append(title)
                news.append("real")
        
        df = pd.DataFrame({'url':articles_url, 'title': titles, 'article': articles, 'news':news})
        df.to_csv(file_name)

if __name__ == "__main__":
    scrapper = HespressScrapper('https://www.hespress.com/politique',200)
    scrapper.save_articles('hespress_politique1.csv')
 



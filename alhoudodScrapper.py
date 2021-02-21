from bs4 import BeautifulSoup
import requests
from urllib.request import Request, urlopen 
import time
import pandas as pd

class AlhoudodScrapper():

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
        divs =  soup.findAll("div", {"class": "elementor-element elementor-element-f785c7f content elementor-widget elementor-widget-theme-post-content"})
        if len(divs) > 0:
            article = divs[0]
            return article.get_text()
        return ""
    
    def get_title(self, soup):
        divs =  soup.findAll("div", {"class": "elementor-element elementor-element-7fc4cdc article-title elementor-widget elementor-widget-heading"})
        if len(divs) > 0:
            title = divs[0]
            return title.get_text()
        return ""
       
    
    def get_articles_url(self):

        articles =[]

        for i in range(1,self.no_of_pagedowns+1):
            url = self.url+"page/"+str(i)+"/"
            print(url)

            soup = self.get_html(url)
            div_articles = soup.findAll("div", {"class": "elementor-posts-container"})[0]
            for link in div_articles.find_all('a'):
                href = link.get('href')
                if href not in articles:
                    articles.append(href)

        return articles
    
    def save_articles(self, file_name):
        articles_url = self.get_articles_url()
        articles = []
        titles = []
        news = []
        hrefs =[]
        for url in articles_url:
            soup = self.get_html(url)
            title = self.get_title(soup)
            article = self.get_article(soup)
            href = url

            if article !="" and title !="":
                articles.append(article)
                titles.append(title)
                news.append("fake")
                hrefs.append(href)

        df = pd.DataFrame({'url':hrefs, 'title': titles, 'article': articles, 'news':news})
        df.to_csv(file_name)

if __name__ == "__main__":
    scrapper = AlhoudodScrapper('https://www.alhudood.net/category/politics/',84)
    scrapper.save_articles("alhoudod.csv")
 



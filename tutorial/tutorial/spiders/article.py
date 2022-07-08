import re
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from tutorial.items import Article
from scrapy.exceptions import CloseSpider
from bs4 import BeautifulSoup


class ArticleSpider(CrawlSpider):#
    n = 0
    name = "article"
    allowed_domains = ["bbc.com"]
    start_urls = ["https://www.bbc.com/news/business"]
    # allowed_domains = ["github.com"]
    # start_urls = ["https://github.com/django/django"]
    rules = [Rule(LinkExtractor(allow=r"/news/business*"), callback="parse_items", follow=True)]

    # def start_requests(self):
    #     urls = [
    #         "https://en.wikipedia.org/wiki/Copyright"
    #     ]

    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)
    
    # def parse(self, response):
    #     url = response.url
    #     title = response.css("h1::text").extract_first()
    #     body = response.css("p::text").extract()
    #     print("///////////////////////////")
    #     print("URL is: {}".format(url))
    #     print("Title is {}".format(title))
    #     print(f"body: {body}")
    
    def parse_items(self, response):
        article = Article()
        article["url"] = response.url
        article["title"] = response.css("h1::text").extract_first()
        article["text"] = response.css("p::text").extract()
        # soup = BeautifulSoup(response.body, 'html.parser')

        # method 1: split lines
        # lines = soup.get_text().splitlines()
        # text = []
        # for line in lines:
        #     line = re.sub(pattern='<.*?>', repl="", string=line)
        #     line = re.sub(pattern='\n', repl="", string=line)
        #     if len(line) > 1:
        #         line = re.sub(pattern="\\s+", repl=" ", string=line)
        #         text.append(line)
        # print(text)

        # method 2: entire text
        # body = re.sub(pattern='<.*?>', repl="", string=str(soup.body))
        # body = re.sub(pattern='\n', repl="", string=body)
        # text = re.sub(pattern="\\s+", repl=" ", string=body)

        # article["text"] = text

        # print(text)
        if self.n == 20000:
            raise CloseSpider
        else:
            self.n += 1
            return article
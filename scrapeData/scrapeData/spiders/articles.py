import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from bs4 import BeautifulSoup
import os
import re
from string import punctuation


class ArticleSpider(CrawlSpider):
    n = 0
    name = "article"
    allowed_domains = ["github.com"]
    start_urls = ["https://github.com/django/django"]
    rules = [Rule(LinkExtractor(allow=r""), callback="parse_items", follow=True)]
    
    def parse_items(self, response):
        title = response.css("h1::text").extract_first()
        soup = BeautifulSoup(response.body, 'html.parser')
        text = soup.get_text()

        title = re.sub(pattern=f"[{punctuation}]", repl="_", string=title)
        title = re.sub(pattern=r"\s", repl="_", string=title)

        print(os.path.join(os.getcwd(), "data_github", f"{title}.txt"))
        with open(os.path.join(os.getcwd(), "data_github", f"{title}.txt"), "w") as f:
            f.write(text)
        if self.n == 200_000:
            raise CloseSpider
        else:
            self.n += 1
            return text

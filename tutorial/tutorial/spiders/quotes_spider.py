import scrapy
from bs4 import BeautifulSoup


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = []
        url = 'https://www.bbc.co.uk/news/world-us-canada-'
        for i in range(59989496, 59989497):
            urls.append(url + str(i))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        url = response.url
        title = response.css('h1::text').extract_first()
        print(url)
        print(title)
        # page = response.url.split("/")[-2]
        # filename = f'quotes-{page}.html'
        # with open(filename, 'wb') as f:
        #     the name of the tag
        #     print(soup.title.name)
            
        #     # Getting the name of parent tag
        #     print(soup.title.parent.name)
        #     f.write(response.body)
        # # self.log(f'Saved file {filename}') # Parsing the HTML
        #     soup = BeautifulSoup(response.body, 'html.parser')
        #     # Getting the title tag
        #     print("/////////////////////////")
        #     print(soup.title)
            
        #     # Getting
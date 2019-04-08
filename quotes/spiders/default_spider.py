import scrapy
import urllib


class QuotesSpider(scrapy.Spider):
    name = "default"

    def start_requests(self):
        urls = [
            'https://www.brainyquote.com/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        links = response.xpath("//span[@class='bq-tn-wrap']/a/@href").extract()
        for link in links:
            absolute_url = urllib.parse.urljoin(response.url, link)
            yield scrapy.Request(absolute_url, callback=self.parse_alphabet)

    def parse_alphabet(self, response):
        author_link = response.xpath("//td/a/@href").extract()
        for author in author_link:
            absolute_url = urllib.parse.urljoin(response.url, author)
            yield scrapy.Request(absolute_url, callback=self.parse_author)
        next_btn = response.xpath("//li/a[contains(text(),'Next')]/@href").extract()[0]
        if next_btn:
            yield scrapy.Request("https://www.brainyquote.com" + str(next_btn[0]), callback=self.parse_alphabet)


    def parse_author(self, request):
        yield {"author" : request.url}

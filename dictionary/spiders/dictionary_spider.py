import scrapy
import urllib
import json
import time

abs_url = "https://www.dictionary.com"


class DictionarySpider(scrapy.Spider):
    name = "dictionary"

    def start_requests(self):
        urls = [
            'https://www.dictionary.com/list/a',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_alphabets)

    def parse_alphabets(self, response):
        ol = response.xpath("//ol")[0]
        alphabet_links = ol.xpath("li/a/@href").extract()
        for alphabet_link in alphabet_links:
            absolute_url = urllib.parse.urljoin(response.url, alphabet_link)
            yield scrapy.Request(url=absolute_url, callback=self.parse_words)

    def parse_words(self, response):
        words_link = response.xpath("//ul[@class='css-8j2tgf e1j8zk4s0']/li/a/@href").extract()
        for word in words_link:
            yield scrapy.Request(url = word, callback=self.parse_word_detail)
        next_page = response.xpath("//li[@class='css-g41ww2 e1wvt9ur5']/a/@href").extract_first()
        if next_page:
            yield scrapy.Request(url = abs_url+next_page, callback=self.parse_words)


    def parse_word_detail(self, response):
        meaning_array = response.xpath("//div[@value='1']/span/text()").extract()
        meaning = ""
        for line in meaning_array:
            meaning = meaning + line
        word = response.xpath("//h1[@class='css-1k2yjrv e1rg2mtf8']/text()").extract_first()
        if word:
            yield {
                "word": word,
                "meaning": meaning,
                "url": response.url,
            }

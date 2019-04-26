import scrapy
import urllib
import json


class ActorSpider(scrapy.Spider):
    name = "actor"

    def start_requests(self):
        urls = [
			'https://en.wikipedia.org/wiki/List_of_Bollywood_actors',
			'https://en.wikipedia.org/wiki/List_of_Indian_film_actresses',
			]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
    	actors_list = response.xpath("//ul/li/a/@href").extract()
    	ind = 0
    	for i in range(len(actors_list)):
    		if "List" in actors_list[i]:
    			ind = i
    			break
    	actors_list = actors_list[:ind]
    	for actor in actors_list:
            absolute_url = urllib.parse.urljoin(response.url, actor)
            yield scrapy.Request(url=absolute_url, callback=self.parse_actor)

    def parse_actor(self, response):
    	name = response.xpath("//h1[@id='firstHeading']/text()").extract_first()
    	bday = response.xpath("//span[@class='bday']/text()").extract_first()
    	yield {
    		"name": name,
    		"bday": bday,
    	}

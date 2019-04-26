import scrapy
import urllib
import json


class ZigWheelsSpider(scrapy.Spider):
    name = "zigwheels"

    def start_requests(self):
        urls = [
            'https://www.zigwheels.com/newcars',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_brands)

    def parse_brands(self, response):
        brand_link = response.xpath("//ul[@id='zwn-brandslider']//a/@href").extract()
        for brand in brand_link:
            absolute_url = urllib.parse.urljoin(response.url, brand)
            if "robots" not in absolute_url:
                print("\n\n" + str(absolute_url) + "\n\n")
                yield scrapy.Request(absolute_url, callback=self.brand_fetch)

    def brand_fetch(self, response):
        item_list = response.xpath("//div[contains(@class, 'nw-serachWrap')]")
        for item in item_list:
            image_url = item.xpath("div/div/a/img/@src").extract_first()
            try:
                car_name = item.xpath("div//h3/text()").extract_first()
            except:
                car_name = "None"
            try:    
                price = item.xpath("div/div[@class='m-info-w']/p/text()").extract_first()
            except:
                price = "Not Available"
            try:
                cc = item.xpath("div/div[@class='m-info-w']/ul/li/span[@class='pull-left ml-5']/text()").extract()[0]
            except:
                cc = "Not available"
            try:
                mileage = item.xpath("div/div[@class='m-info-w']/ul/li/span[@class='pull-left ml-5']/text()").extract()[1]
            except:
                mileage = "Not available"
            try:    
                fuel = item.xpath("div/div[@class='m-info-w']/ul/li/span[@class='pull-left ml-5']/text()").extract()[2]
            except:
                fuel = "Not Available"
            try:
                type_car = item.xpath("div/div[@class='m-info-w']/ul/li/span[@class='pull-left ml-5']/text()").extract()[3]
            except:
                type_car = "Non Manual"
            yield{
                "image": image_url,
                "car_name": car_name,
                "price": price,
                "cc": cc,
                "mileage": mileage,
                "fuel": fuel,
                "type_car": type_car,
            }

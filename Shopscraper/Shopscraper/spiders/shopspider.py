# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from Shopscraper.items import ShopscraperItem
import json
import requests

class ShopspiderSpider(scrapy.Spider):
    name = "shopspider"
    allowed_domains = ["openingstijden.nl"]
    start_urls = (
        'https://www.openingstijden.nl/Telefoon-en-Mobiel/',
    )

    def parse(self, response):
        
        for stores in response.xpath('//div[@class="my-location spacer"]/ul/li') :

            item = ShopscraperItem()

            item['Name']    = ' '.join(stores.xpath('h3/a/text()').extract()).strip()
            # self.logger.info( name )
            item['Address'] = ' '.join(stores.xpath('h3/a/span/text()').extract()).strip()
            # self.logger.info( address )
            item['City']    = ' '.join(stores.xpath('h3/a/cite/text()').extract()).strip()
            # self.logger.info( city )
            yield item

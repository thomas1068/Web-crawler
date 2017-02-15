# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from Bedrijscraper.items import BedrijscraperItem
import requests
# import proxylist
import re, random, base64

class BedrijspiderSpider(scrapy.Spider):
    name = "bedrijspider"
    allowed_domains = ["bedrijvenpagina.nl"]
    start_urls = (
        'https://www.bedrijvenpagina.nl/beauty-en-verzorging/',
    )

    # proxy_lists = proxylist.proxys

    # def set_proxies(self, url, callback):
    #     req = Request(url=url, callback=callback, dont_filter=True)
    #     proxy_url = self.proxy_lists[random.randrange(0,100)]
    #     req.meta.update({'proxy': "https://" + proxy_url})
    #     user_pass=base64.encodestring(b'user:p19gh1a').strip().decode('utf-8')
    #     req.headers['Proxy-Authorization'] = 'Basic ' + user_pass

        # user_agent = self.ua.random
        # req.headers['User-Agent'] = user_agent

        # req.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        # req.headers['Accept-Encoding'] = 'gzip, deflate'
        # req.headers['Accept-Language'] = 'en-US,en;q=0.8'
        # #req.headers['Cache-Control'] = 'max-age=0'
        # #req.headers['Connection'] = 'keep-alive'
        # #req.headers['Content-Length'] = '10'
        # req.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        # #req.headers['Cookie'] = 'PHPSESSID=hpfta0h8imb3ma3obdp2vrc0d5; md5key=6f6c7f62bc57227e14c85c85d117c591; CNZZDATA5849826=cnzz_eid%3D326421496-1485428248-%26ntime%3D1485523483'
        # req.headers['Host'] = 'www.usbizs.com'
        # req.headers['Origin'] = "http://www.usbizs.com"
        # req.headers['Upgrade-Insecure-Requests'] = "1"
        # print ('&&&&&&&&&&&&&&&&&&&&&&&&&', url)
        # return req

    def start_requests(self):
        # self.ua = UserAgent()
        start_url = self.start_urls[0]
        yield self.set_proxies(start_url, self.parse_item)
        #yield self.set_proxies(start_url, self.parse_detail)

    def parse(self, response):
        yield Request(response.url, self.parse_item)


    # def parse_item(self, response):
    def parse(self, response):
        for stores_url in response.xpath('//div[@class="col-xs-12 col-md-8"]/main/div[@class="box clearfix bedrijven"]/div[@class="bedrijf"]') :
            store_url = response.urljoin(stores_url.xpath('ul[@class="pull-left"]/li[@class="bedrijfsbuttons"]/a[@class="btn btn-success meer-info"]/@href')[0].extract())
            # self.logger.info( store_url )
            req = Request(url=store_url, callback=self.store_detail)
            # req.meta['url'] = store_url
            yield req

        next_page = response.xpath('//div[@class="pagers"]//li[@class="next"]/a/@href').extract()

        if ( len(next_page) == 1 ) :

            # reqt = self.set_proxies(url='https://www.bedrijvenpagina.nl' + next_page[0], callback=self.parse_item)
            # yield reqt

            yield Request(url='https://www.bedrijvenpagina.nl' + next_page[0], callback=self.parse, dont_filter=True)
    def store_detail(self, response):
        # self.logger.info( "-----------------------------" )
        # self.logger.info( response )
        detail_path = response.xpath('//div[@class="row content"]//div[@class="card"]')
        item = BedrijscraperItem()
               
        item['Name'] = ' '.join(detail_path.xpath('span[@class="hidden"]/text()').extract()).strip()
        item['Address'] = ' '.join(detail_path.xpath('div[@class="adr"]/span[@class="street-address"]/text()').extract()).strip()
        item['Postal'] = ' '.join(detail_path.xpath('div[@class="adr"]/span[@class="postal-code"]/text()').extract()).strip()
        item['City'] = ' '.join(detail_path.xpath('div[@class="adr"]/span[@class="locality"]/text()').extract()).strip()       
        # country = detail_path.xpath('div[@class="adr"]/span[@class="country-name hidden"]/text()').extract()
        item['Email'] = ' '.join(detail_path.xpath('div[@class="mail"]/a/text()').extract()).strip()       
        item['Web'] = ' '.join(detail_path.xpath('div[@class="url"]/a/text()').extract()).strip()        
        item['KVK'] = ' '.join(detail_path.xpath('div[@class="kvk"]/a/text()').extract()).strip()
        yield item

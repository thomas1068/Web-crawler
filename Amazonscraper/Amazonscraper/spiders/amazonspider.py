# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from Amazonscraper.items import AmazonscraperItem
import requests
import proxylist
import re, random, base64

class AmazonspiderSpider(scrapy.Spider):
    name = "amazonspider"
    allowed_domains = ["amazon.com"]
    start_urls = (
        'https://www.amazon.com/gp/offer-listing/B0000002L9/ref=olp_f_new?ie=UTF8&f_new=true',
        'https://www.amazon.com/gp/offer-listing/B0000002L9/ref=olp_f_usedLikeNew?ie=UTF8&f_usedLikeNew=true',
        'https://www.amazon.com/gp/offer-listing/B0000002L9/ref=olp_f_usedVeryGood?ie=UTF8&f_usedVeryGood=true',
        'https://www.amazon.com/gp/offer-listing/B0000002L9/ref=olp_f_usedGood?ie=UTF8&f_usedGood=true',
    )

    proxy_lists = proxylist.proxys

    def set_proxies(self, url, callback):
        req = Request(url=url, callback=callback, dont_filter=True)
        proxy_url = self.proxy_lists[random.randrange(0,100)]
        req.meta.update({'proxy': "https://" + proxy_url})
        user_pass=base64.encodestring(b'user:p19gh1a').strip().decode('utf-8')
        req.headers['Proxy-Authorization'] = 'Basic ' + user_pass

        # user_agent = self.ua.random
        # req.headers['User-Agent'] = user_agent

        # req.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        # req.headers['Accept-Encoding'] = 'gzip, deflate'
        # req.headers['Accept-Language'] = 'en-US,en;q=0.8'
        #req.headers['Cache-Control'] = 'max-age=0'
        #req.headers['Connection'] = 'keep-alive'
        #req.headers['Content-Length'] = '10'
        # req.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        # #req.headers['Cookie'] = 'PHPSESSID=hpfta0h8imb3ma3obdp2vrc0d5; md5key=6f6c7f62bc57227e14c85c85d117c591; CNZZDATA5849826=cnzz_eid%3D326421496-1485428248-%26ntime%3D1485523483'
        # req.headers['Host'] = 'www.usbizs.com'
        # req.headers['Origin'] = "http://www.usbizs.com"
        # req.headers['Upgrade-Insecure-Requests'] = "1"
        # print ('&&&&&&&&&&&&&&&&&&&&&&&&&', url)
        return req

    def start_requests(self):


        category = [
        'f_new',
        'f_usedLikeNew',
        'f_usedVeryGood',
        'f_usedGood',
        ]
        # self.ua = UserAgent()
        for i in range(0, 4):
            # start_url = self.start_urls[i]
            # ccc =  category[i]
            # self.logger.info( ccc )

            start_url = "https://www.amazon.com/gp/offer-listing/B0000002L9/ref=olp_" + category[i] + "?ie=UTF8&" + category[i] + "=true"
            
            reqa = self.set_proxies(start_url, self.parse_item)
            reqa.meta['categor'] = category[i]
            yield reqa
        #yield self.set_proxies(start_url, self.parse_detail)

    # def parse(self, response):
    #     yield Request(response.url, self.parse_item)

    def parse_item(self, response):

        cate = response.meta['categor']

        url_paths = response.xpath('//div[@class="a-section a-spacing-double-large"]/div[@class="a-row a-spacing-mini olpOffer"]')

        item = AmazonscraperItem()
        if (cate == "f_new"):
            item['Category'] = "New"

        if (cate == "f_usedLikeNew"):
            item['Category'] = "LikeNew"

        if (cate == "f_usedVeryGood"):
            item['Category'] = "VeryGood"

        if (cate == "f_usedGood"):
            item['Category'] = "Good"

        for url_path in url_paths:

            url_buf = url_path.xpath('div[@class="a-column a-span2 olpSellerColumn"]/h3/span/a/@href').extract()
            if url_buf:

                url = "https://www.amazon.com" + url_buf[0]
                item['Url'] = url

                # self.logger.info( "-----------------------------" )
                # self.logger.info( url )
                yield item
        next_page  = response.xpath('//div[@class="a-text-center a-spacing-large"]/ul[@class="a-pagination"]/li[@class="a-last"]/a/@href').extract()

        if ( len(next_page) == 1 ) :

            req = self.set_proxies(url='https://www.amazon.com/' + next_page[0], callback=self.parse_item)
            req.meta["categor"] = response.meta["categor"]
            yield req

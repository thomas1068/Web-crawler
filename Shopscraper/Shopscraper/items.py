# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ShopscraperItem(scrapy.Item):

    City      = scrapy.Field()
    Name      = scrapy.Field()
    Address   = scrapy.Field()

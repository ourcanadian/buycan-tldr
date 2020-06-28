# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import SitemapSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import SrcItem
import re

'''
Generic Command: 
    scrapy crawl about

Output to FILENAME (.csv or .json)
    scrapy crawl about -o FILENAME

'''

TMP_TXT_FILE = './buycan-tldr-TMP.txt'

class AboutSpider(SitemapSpider):
    name = 'about'
    url = open(TMP_TXT_FILE).read()
    allowed_domains = [re.sub('http[s]?://', '', url)]
    sitemap_urls = [url+"/robots.txt"]

    sitemap_rules = [('about', 'parse_item'), ('story', 'parse_item')]

    def sitemap_filter(self, entries):
        for entry in entries:
            yield entry

    def parse_item(self, response):
        items = SrcItem()
        items['url'] = response.request.url
        items['text'] = response.xpath(
                '''
                    //p/text() | 
                    //span/text() | 
                    //h1/text() | 
                    //h2/text() | 
                    //h3/text() | 
                    //h4/text() |
                    //h6/text()
                '''
            ).extract()
        yield items

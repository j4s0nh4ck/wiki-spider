# -*- coding: utf-8 -*-
import scrapy

from wiki.items import WikiItem 
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
#from scrapy.sgml import SgmlLinkExtractor 
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
import re

class LocalwikiSpider(scrapy.Spider):
    name = "localwiki"
    allowed_domains = ["10.100.1.22"]
    start_urls = (
        'http://10.100.1.22/',
    )
    rules = (
#        Rule(LinkExtractor(deny_extensions =('ico', ), allow=(r'.*',))),
#        Rule(LxmlLinkExtractor(deny=(r'.*mediawiki.*', )))
#        Rule(SgmlLinkExtractor(deny=(r'.*mediawiki.*', )))
#        Rule(LinkExtractor(deny_extensions=('php', ), allow=(r'.*', ))),
#        Rule(LinkExtractor(deny=(r'action\=history', ), allow=(r'.*', )))
        Rule(LinkExtractor(deny =(r'mediawiki', ), allow=(r'/',))),
    )
    def __init__(self, *a, **kw):
        super(LocalwikiSpider, self).__init__(*a, **kw)
        self.all_urls = set()
        self.regex = re.compile(r'.*(mediawiki|WhatLinksHere).*')
    def parse(self, response):
        hrefs = set(filter(lambda s: (s[0] == "/") and (s != '/favicon.ico') and ( not self.regex.search(s)) ,response.selector.xpath("//@href").extract()))
        for href in hrefs:
            if href in self.all_urls:
                continue
            self.all_urls.add(href)
            url = response.urljoin(href)
            self.log("In parser:\t\t" + url + "\n")
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        item = WikiItem()
        item['title'] = response.selector.xpath("//title/text()").extract()[0]
        item['link'] = response.request.url
        yield item

        hrefs = set(filter(lambda s: (s[0] == "/") and (s != '/favicon.ico') and (not self.regex.search(s)), response.selector.xpath("//@href").extract()))
        
        for href in hrefs:
            if href in self.all_urls:
                continue
            url = response.urljoin(href)
#            self.log("In parse_dir_contents:\t\t" + url + "\n")
#            self.log("In parse_dir_contents:\t original url: %s\t current url: %s" %(response.request.url, url))
            yield scrapy.Request(url, callback=self.parse_dir_contents)

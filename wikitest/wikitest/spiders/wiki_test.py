import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import logging
class MySpider(CrawlSpider):
    name = 'wikitest'
    allowed_domains = ['10.100.1.22']
    start_urls = ['http://10.100.1.22/Main_Page']

    rules = (
        Rule(LinkExtractor(allow=('Process$', )), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        logging.warning('Hi, this is an item page! %s', response.url)
        item = scrapy.Item()
        logging.warning("in parser_item...")
        return item

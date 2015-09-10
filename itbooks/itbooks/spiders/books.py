# -*- coding: utf-8 -*-
#####################################################################
# Refer to https://codexcipher.wordpress.com/2014/04/11/some-sensational-scrapy-stuff/
#####################################################################
'''
import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["it-ebooks.info"]
    start_urls = (
        'http://www.it-ebooks.info/',
    )

    def parse(self, response):
        pass
'''
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
#from scrapy.linkextractors.sgml import SgmlLinkExtractor
from itbooks.items import ItbooksItem
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor 
import logging
from scrapy.utils.log import configure_logging
from scrapy.shell import inspect_response


configure_logging(install_root_handler=False)
logging.basicConfig(
    filename='log.txt',
    format='%(levelname)s: %(message)s',
    level=logging.WARNING
)
class ItbooksSpider(CrawlSpider):
    name = "itbooks"
    allowed_domains = ["it-ebooks.info"]
    start_urls = ["http://it-ebooks.info/tag/programming/"]
 
    rules = (
#        Rule(SgmlLinkExtractor(allow=(r"page\/\d+\/$",), ), callback="parse_start_url", follow=True ),
#        Rule(LinkExtractor(allow=(r"page\/\d+\/$",), ), callback="parse_start_url_a", follow=False ),
        Rule(LinkExtractor(allow=(r"page\/\d+\/$",), ), callback="parse_start_url_a", follow=True ),
#         Rule(LinkExtractor(allow=(r"page\/\d+\/$",), ),),
        Rule(LinkExtractor(allow=(r"book\/\d+\/$",), ), callback="parse_item", follow=False ),
    )
 
    def parse_start_url_a(self, response):
#        sel = Selector(response)
#        links = sel.xpath("//td[@width='200']/a/@href").extract()
        logging.warning("in parse_start_url_a, and the url is:\t" + response.url)
#        for link in links:
#            url = "http://it-ebooks.info%s" % link
#            rq = Request(url, callback=self.parse_item)
#            yield rq

    def parse_start_url(self, response):
        sel = Selector(response)
        links = sel.xpath("//td[@width='200']/a/@href").extract()
        logging.warning("in parse_start_url, and the url is:\t" + response.url)
        for link in links:
            url = "http://it-ebooks.info%s" % link
            rq = Request(url, callback=self.parse_item)
            yield rq

    def parse_item(self, response):
        logging.warning("in parse_item, and the url is:\t" + response.url)
        sel = Selector(response)
        item = ItbooksItem()
        item["title"] = sel.xpath("//h1[@itemprop='name']/text()").extract()
        item["subtitle"] = sel.xpath("//h1[@itemprop='name']/following::h3/text()").extract()
#        inspect_response(response, self)
        yield item


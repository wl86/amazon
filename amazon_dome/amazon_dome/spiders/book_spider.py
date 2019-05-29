# -*- coding: utf-8 -*-
import time

import scrapy
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class BookSpiderSpider(CrawlSpider):
    name = 'book_spider'
    allowed_domains = ['category.dangdang.com']
    start_urls = ['http://category.dangdang.com']

    rules = (
        Rule(LinkExtractor(allow=r'category.dangdang.com/cp01.00.00.00.00.00.html'), callback='parse_item',
             follow=True),
    )

    def parse_item(self, response):
        '''
        所有书籍分类
        :param response:
        :return:
        '''
        # 文学
        literature = response.xpath("//div[@class='clearfix']/span[9]/a/@title").extract_first()
        # 文学url
        literature_url = 'http://category.dangdang.com/' + response.xpath("//div[@class='clearfix']/span[9]/a/@href").extract_first()
        print(literature,literature_url)

        r = Request(url=literature_url, callback=self.classify_item, dont_filter=True)
        yield r

    def classify_item(self, response):
        '''
        文学类书籍
        :param response:
        :return:
        '''
        book_list = response.xpath("//p[@class='name']/a/@href").extract()
        for i in range(0, len(book_list) -1):
            book_url = book_list[i]

            r = Request(url=book_url, callback=self.details_item, dont_filter= True)

            yield r


    def details_item(self, response):
        # 书名
        book_name = response.xpath("//div[@class='name_info']/h1/@title").extract_first()
        print(book_name,response.url)
        BookImgList = response.xpath(f"//ul[@id='main-img-slider']/li[6]/a/img/@src").extract_first()
        print(BookImgList)


# -*- coding: utf-8 -*-
import time

import scrapy
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from amazon_dome.utils.bshead import create_bs_driver


class AmazonSpiderSpider(CrawlSpider):
    name = 'amazon_spider'
    allowed_domains = ['www.amazon.cn']
    start_urls = ['https://www.amazon.cn']

    rules = (
        # 获取所有分类url
        Rule(LinkExtractor(allow=r'amazon.cn/gp/site-directory/ref=nav_shopall_btn/'), callback='parse_item',
             follow=True),
    )

    # def __init__(self):
    #     CrawlSpider.__init__(self, self.name)
    #     self.driver = create_bs_driver()
    #     self.driver.set_page_load_timeout(20)
    #
    # def __del__(self):
    #     self.driver.quit()

    def parse_item(self, response):
        # 美妆
        beauty_makeup_title = response.xpath("//div[@id='cat8']/div/span/a[1]/text()").extract_first()
        # 面部护肤
        moisturizing_title = response.xpath("//div[8]/div[2]/div[1]/div[2]/div/span/a/text()").extract_first()
        moisturizing_list = response.xpath("//div[8]/div[2]/div[1]/div[2]/div/div/ul/li/span/span/a/text()").extract()
        for i in range(1,len(moisturizing_list) + 1):

            # 洁面
            face_washing_title = response.xpath(
                f"//div[8]/div[2]/div[1]/div[2]/div/div/ul/li[{i}]/span/span/a/text()").extract_first()
            # 洁面url
            face_washing_url = 'https://www.amazon.cn' + response.xpath(
                f"//div[8]/div[2]/div[1]/div[2]/div/div/ul/li[{i}]/span/span/a/@href").extract_first()
            print(beauty_makeup_title, moisturizing_title, face_washing_title, face_washing_url)
            # 发射洁面url,爬取所有洁面商品
            r = Request(url=face_washing_url, callback=self.beauty_item, dont_filter=True)
            yield r

    def beauty_item(self, response):
        # 商品的url
        # time.sleep(2)
        commodity_list = response.xpath("//div[2]/ul/li/div/div[3]/div[1]/a/@href").extract()
        for j in range(1, len(commodity_list) + 1):
            commodity_url = response.xpath(f"//div[2]/ul/li[{j}]/div/div[3]/div[1]/a/@href").extract_first()
            if commodity_url:
                print(commodity_url)
                r = Request(url=commodity_url, callback=self.commodity_item, dont_filter=True)
                yield r
            else:
                continue

    def commodity_item(self, response):
        commodity = response.xpath("//span[@id='productTitle']/text()").extract_first()
        commodity_name = commodity.strip()
        print(commodity_name)




# -*- coding: utf-8 -*-
import scrapy
from ..items import EbayItem


class EbaySpider(scrapy.Spider):
    name = "ebay"
    allowed_domains = ["ebay.co.uk"]
    start_urls = ['https://www.ebay.co.uk/v/allcategories']

    def parse(self, response):
        urls = response.xpath('//li[@class="sub-category"]/a/@href').extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.individual_page)

    def individual_page(self, response):
        parent_url = response.url
        boxs = response.xpath('//li[@class="s-item"]')
        for box in boxs:
            id = box.xpath('.//a[@class="s-item__link"]/@href').re_first(r"^.+?/(\d+)\?.+$")
            name = box.xpath('.//h3[@class="s-item__title"]/text()').extract_first()
            orders = box.xpath('.//span[@class="NEGATIVE"]/text()').re_first(r"(\d+,*\d*) sold")
            if orders != None:
                orders = orders.replace(',', '')
            full_url = box.xpath('.//a[@class="s-item__link"]/@href').extract_first()

            fields = EbayItem(id=id, name=name, orders=orders, url=full_url, parent_url=parent_url)

            yield fields

            # Calling next page
            next_page_url = response.xpath('//a[@rel="next"]/@href').extract_first()
            yield scrapy.Request(next_page_url, callback=self.individual_page)
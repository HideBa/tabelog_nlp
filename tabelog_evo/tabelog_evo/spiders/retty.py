# -*- coding: utf-8 -*-
import scrapy
from ..middlewares import close_driver
from tabelog_evo.items import RettyItem
import time

class RettySpider(scrapy.Spider):
    name = 'retty'
    allowed_domains = ['retty.me']
    #start_urls = ['https://retty.me/restaurant-search/search-result/?&category_type=30&min_budget=1&max_budget=13&free_word_category=%E5%AF%BF%E5%8F%B8']
    url_format = 'https://retty.me/restaurant-search/search-result/?page={}&free_word_category=%E5%AF%BF%E5%8F%B8&category_type=30&min_budget=1&max_budget=13'
    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            "tabelog_evo.middlewares.SeleniumMiddleware": 0,
        },
        "DOWNLOAD_DELAY" : 5,
    }

    def __init__(self, page_limit=3):
        self.page_limit = int(page_limit)

    def start_requests(self):
        for i in range(1, self.page_limit+1):
            url = self.url_format.format(str(i))
            request = scrapy.Request(url=url, callback=self.parse)
            yield request

    def parse(self, response):
        url_list = response.css('a.restaurant__block-link::attr("href")').getall()
        for url in url_list:
            item = RettyItem()
            item['url'] = url
            time.sleep(2)
            request = scrapy.Request(
                url,
                callback=self.parse_store
                )
            request.meta['item'] = item
            time.sleep(2)
            yield request
        #self.closed()
    
    def parse_store(self, response):
        item = response.meta['item']

        name = response.css('span.restaurant-summary__display-name').xpath("string()").get().strip()
        item['name'] = name

        phone_num = response.css('span.restaurant-actions__tel-number').xpath("string()").get()
        item['phone_num'] = phone_num

        wannago = response.css('span.wannago-button__label.wannago-button__label--bold').xpath("string()").getall()[1].strip()
        item['wannago'] = wannago

        yield item

    def closed(self, response):
        close_driver()
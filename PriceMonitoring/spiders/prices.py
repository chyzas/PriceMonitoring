import scrapy
from PriceMonitoring.items import PricemonitoringItem
from PriceMonitoring.models import *
from scrapy import Request


class PricesSpider(scrapy.Spider):
    name = "prices"

    def start_requests(self):
        items = Items.select()
        for item in items:
            yield Request(item.url, meta={'item_id': item.id, 'name': item.name, 'xpath': item.price_xpath})

    def parse(self, response):
        xpath = response.meta['xpath'] + '/text()'
        item = PricemonitoringItem()
        item['price'] = response.xpath(xpath).extract_first()
        item['item_id'] = response.meta['item_id']
        item['name'] = response.meta['name']
        yield item

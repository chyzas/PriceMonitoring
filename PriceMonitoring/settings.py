# -*- coding: utf-8 -*-


BOT_NAME = 'PriceMonitoring'

SPIDER_MODULES = ['PriceMonitoring.spiders']
NEWSPIDER_MODULE = 'PriceMonitoring.spiders'



USER_AGENT = "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"


ITEM_PIPELINES = {
   'PriceMonitoring.pipelines.PricemonitoringPipeline': 1,
}

MAIL = {
    'server': '',
    'user': '',
    'pass': '',
    'port': 587,
    'from': '',
    'to': ''
}


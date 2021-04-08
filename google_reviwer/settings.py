# -*- coding: utf-8 -*-

# Scrapy settings for goodreader project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
BOT_NAME = 'google_reviwer'
SPIDER_MODULES = ['google_reviwer.spiders']
NEWSPIDER_MODULE = 'google_reviwer.spiders'
DOWNLOADER_MIDDLEWARES = {'scrapy_crawlera.CrawleraMiddleware': 300,}
CRAWLERA_ENABLED = True
CRAWLERA_APIKEY = 'abac66ba77b14573b5c9520dcc93b10c'
ROBOTSTXT_OBEY = False
#CONCURRENT_REQUESTS = 50
#CONCURRENT_REQUESTS_PER_DOMAIN = 50
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
#AUTOTHROTTLE_ENABLED = False
#DOWNLOAD_TIMEOUT = 600

'''
CONCURRENT_REQUESTS = 10
CONCURRENT_REQUESTS_PER_DOMAIN = 10
AUTOTHROTTLE_ENABLED = False
DOWNLOAD_TIMEOUT = 600
'''

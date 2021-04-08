# Imports - isort result
import datetime 

import json
import random
import re
from collections import OrderedDict
from urllib import parse
from urllib.parse import urlparse
#import certifi
import requests
import scrapy
from pyquery import PyQuery
from requests.adapters import HTTPAdapter
import datetime
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]   
user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=500)
import pkgutil


class GoogleScraperBusiness(scrapy.Spider):
  name = "googlereviwer_spider"
  business_id = ''
  review_count = ''
  #review_pages = ''
  domain_name= ''
  business_url= ''

  def __init__(self, *args, **kwargs):
    self.start_urls =pkgutil.get_data("google_reviwer", "resources/url.csv").decode('latin-1').splitlines()
    self.business_url = ''
  def start_requests(self):
    headers =  {'User-Agent':user_agent_rotator.get_random_user_agent() }
    for page in self.start_urls:
      self.business_url = page
      request = scrapy.Request(page, method='GET',headers=headers, callback=self.parse )
      yield request

  def parse(self, response):
    headers =  {'User-Agent':user_agent_rotator.get_random_user_agent() }
    res = PyQuery(response.body)('script:contains("window.APP_INITIALIZATION_STATE")').text().split(";window.APP_INITIALIZATION_STATE=")[1].split(";window.APP_FLAGS=")[0]
    JSON_request_variables =json.loads(res)
    new_json = json.loads(JSON_request_variables[3][6].replace(")]}'",""))
    JSON_request_variables2 = new_json[6][72][0][0][29]
    try:
      Phone = new_json[6][178][0][0]
    except:
      Phone = ''
    try :
      Website = new_json[6][7][0] 
    except:
      Website = ''
    try:
      Business_Rating_Value = new_json[6][4][7]
    except:
      Business_Rating_Value = ''

    try:
      Business_Reviews_Count = new_json[6][4][8]
    except:
      Business_Reviews_Count = ''

    item= { 'URL':response.request.url,
    'Business_ID':response.request.url.split('cid=')[-1],
    'Name':new_json[6][11],
    'Phone': Phone,
    'Address':new_json[6][39],
    'Website':Website,
    'Business_Rating_Value':Business_Rating_Value,
    'Business_Reviews_Count':Business_Reviews_Count,
    }
    page =f'https://www.google.com/maps/preview/review/listentitiesreviews?authuser=0&hl=en&gl=eg&pb=!1m2!1y{JSON_request_variables2[0]}!2y{JSON_request_variables2[1]}!2m2!1i0!2i10!3e4!4m5!3b1!4b1!5b1!6b1!7b1!5m2!1sxpBlYIraEcqc1fAPxPOJqAc!7e81'
    request = scrapy.Request(page, method='GET',headers=headers, callback=self.parse_1 , meta={'item':item})
    yield request
  def parse_1(self, response):
    JSON_Results = json.loads(response.text.replace(")]}'",""))
    item = response.meta['item']
    if JSON_Results[2]!=None:
      for de in JSON_Results[2]:
        item['ReviewID']= de[10]
        item['Reviwer'] = de[0][1]
        try:
          item['ReviwerProfile'] = 'https://www.google.com/maps/contrib/'+de[6]
        except:
          item['ReviwerProfile'] = ''
        item['ReviewDetails'] = de[3]
        item['Date'] = de[1]
        item['Rating'] = de[4]
        second = item['Date'][:-4].split()[1]
        if second.find('month')==-1 & second.find('year')==-1:

          if item['Date'][:-4].split()[0]=='a':
            first = 1
          else:
            first = int(item['Date'][:-4].split()[0])      
          if second[-1]!='s':
            second+='s'
          time_dict = dict((fmt,float(first)) for amount,fmt in [[first , second]])
          dt = datetime.timedelta(**time_dict)
          past_time = datetime.datetime.now() - dt
          item['Date'] = past_time.date()
          Days= dt.days
          if  item['Rating']!=None: 
            if item['Rating']<4 :
              if Days<=14:
                yield item


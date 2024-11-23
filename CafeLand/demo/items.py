# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
class UnitopItem(scrapy.Item):
    project_type = scrapy.Field()
    project_name = scrapy.Field()
    street = scrapy.Field()
    city = scrapy.Field()
    investor = scrapy.Field()
    status = scrapy.Field() # add new
    area = scrapy.Field() # add new
    date = scrapy.Field() # add new
    total_investment = scrapy.Field() # add new
    average_rating = scrapy.Field() # add new
    moTa = scrapy.Field() 